import json
import os
import random
import re
import time
from copy import deepcopy
from io import BytesIO
from pathlib import Path
from typing import List, Optional

import requests
from loguru import logger

from tau2.data_model.audio import AudioData, AudioEncoding, AudioFormat
from tau2.data_model.voice import ElevenLabsTTSConfig
from tau2.utils.language_utils import get_language_code

AUDIO_TAG_PATTERN = re.compile(r"\[(cough|sneeze|sniffle)\]")
PAUSE_TAG_PATTERN = re.compile(r"\[pause\]", re.IGNORECASE)

MAX_API_RETRY = 3
TTS_RETRY_SLEEP = (1, 5)

ASSETS_DIR = Path(__file__).parent / "assets"

_voices_cache: Optional[dict] = None


def _load_voices() -> dict:
    global _voices_cache
    if _voices_cache is None:
        voices_path = ASSETS_DIR / "elevenlabs_voices.json"
        with open(voices_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        _voices_cache = {
            "voices": data["voices"],
            "multilingual_ids": [
                v["voice_id"]
                for v in data["voices"]
                if "eleven_multilingual_v2" in v.get("high_quality_base_model_ids", [])
            ],
            "voices_info": {
                v["voice_id"]: v for v in data["voices"]
            },
        }
    return _voices_cache


def _select_voice_for_language(language_code: str) -> str:
    """Select a voice ID that is verified for the given language code."""
    voices = _load_voices()
    ids = list(voices["multilingual_ids"])
    random.shuffle(ids)
    for vid in ids:
        info = voices["voices_info"][vid]
        for vl in info.get("verified_languages", []):
            if vl.get("language") == language_code:
                return vid
    return random.choice(ids)


def make_elevenlabs_output_format(codec: str, sample_rate: int, bitrate: int) -> str:
    return f"{codec}_{sample_rate}_{bitrate}"


def parse_elevenlabs_output_format(output_format: str):
    pat = re.compile(r"^(\w+)_(\d+)_(\d+)$")
    match = pat.match(output_format)
    if not match:
        raise ValueError(f"Invalid ElevenLabs output format: {output_format}")
    return match.group(1), int(match.group(2)), int(match.group(3))


def tts_elevenlabs(
    text: str,
    config: ElevenLabsTTSConfig,
) -> AudioData:
    """Text to speech using ElevenLabs API via DashScope proxy.

    Uses DASHSCOPE_API_URL and DASHSCOPE_API_KEY environment variables
    to route ElevenLabs requests through a DashScope-compatible endpoint.

    Falls back to the direct ElevenLabs SDK if DASHSCOPE_API_URL is not set.
    """
    dashscope_url = os.getenv("DASHSCOPE_API_URL")
    if dashscope_url:
        return _tts_via_dashscope(text, config, dashscope_url)
    else:
        return _tts_via_sdk(text, config)


def _tts_via_dashscope(
    text: str,
    config: ElevenLabsTTSConfig,
    api_url: str,
) -> AudioData:
    """Call ElevenLabs TTS through DashScope proxy."""
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
        raise ValueError(
            "DASHSCOPE_API_KEY not found. Set it to use ElevenLabs via DashScope."
        )

    language_code = get_language_code()

    voice_id = config.voice_id
    if not voice_id:
        voice_id = _select_voice_for_language(language_code)

    voice_model = "eleven_multilingual_v2"

    text_preview = text[:50] + "..." if len(text) > 50 else text
    logger.debug(
        f"ElevenLabs TTS (DashScope): calling API for text '{text_preview}' "
        f"(voice_id={voice_id}, model={voice_model})"
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "model": voice_model,
        "text": text,
        "voice_id": voice_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
        },
    }

    for attempt in range(MAX_API_RETRY):
        try:
            resp = requests.post(api_url, headers=headers, data=json.dumps(data))
            if resp.status_code == 200 and "data" in resp.json():
                audio_url = resp.json()["data"]
                audio_response = requests.get(audio_url)
                audio_bytes = audio_response.content

                if len(audio_bytes) == 0:
                    raise ValueError("ElevenLabs TTS returned empty audio")

                logger.debug(
                    f"ElevenLabs TTS (DashScope): received {len(audio_bytes)} bytes"
                )

                return AudioData(
                    data=audio_bytes,
                    format=AudioFormat(
                        encoding=AudioEncoding.PCM_S16LE,
                        sample_rate=16000,
                    ),
                )
            else:
                logger.warning(
                    f"ElevenLabs TTS (DashScope) attempt {attempt + 1}: "
                    f"status={resp.status_code}, body={resp.text[:200]}"
                )
        except Exception as e:
            logger.warning(
                f"ElevenLabs TTS (DashScope) attempt {attempt + 1}: {e}"
            )
            time.sleep(random.randint(*TTS_RETRY_SLEEP))

    raise ValueError(f"ElevenLabs TTS (DashScope) failed after {MAX_API_RETRY} attempts")


def _tts_via_sdk(
    text: str,
    config: ElevenLabsTTSConfig,
) -> AudioData:
    """Call ElevenLabs TTS directly using the official SDK (original behavior)."""
    from elevenlabs import ElevenLabs

    api_key = config.api_key or os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in config or environment")

    is_v3 = "v3" in config.model_id.lower()

    if not is_v3 and PAUSE_TAG_PATTERN.search(text):
        text = PAUSE_TAG_PATTERN.sub("...", text)

    if AUDIO_TAG_PATTERN.search(text) and not is_v3:
        logger.warning(
            f"Audio tags detected in text but model is {config.model_id}. "
            "Audio tags like [cough], [sneeze], [sniffle] only work with v3 models."
        )

    client = ElevenLabs(api_key=api_key)
    voice_id = config.voice_id

    text_preview = text[:50] + "..." if len(text) > 50 else text
    logger.debug(
        f"ElevenLabs TTS: calling API for text '{text_preview}' "
        f"(voice_id={voice_id}, model={config.model_id})"
    )

    try:
        audio = client.text_to_speech.convert(
            text=text,
            voice_id=voice_id,
            voice_settings=config.voice_settings,
            model_id=config.model_id,
            output_format=config.output_format_name,
            seed=config.seed,
        )
        audio_bytes = b"".join(audio)
    except Exception as e:
        logger.debug(
            f"ElevenLabs TTS API call failed: {type(e).__name__}: {e} "
            f"(text='{text_preview}', voice_id={voice_id}, model={config.model_id})"
        )
        raise

    logger.debug(f"ElevenLabs TTS: received {len(audio_bytes)} bytes of audio")

    if len(audio_bytes) == 0:
        raise ValueError(f"ElevenLabs TTS returned empty audio for text: '{text}'")

    return AudioData(
        data=audio_bytes,
        format=deepcopy(config.output_audio_format),
    )
