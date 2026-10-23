import os

# ISO 639-1 codes for every evaluated language (22 + English + German).
LANGUAGE_NAME_TO_CODE = {
    "Arabic": "ar",
    "Belarusian": "be",
    "Burmese": "my",
    "Chinese": "zh",
    "Eastern Panjabi": "pa",
    "English": "en",
    "French": "fr",
    "German": "de",
    "Hebrew": "he",
    "Hindi": "hi",
    "Indonesian": "id",
    "Japanese": "ja",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Lao": "lo",
    "Malay": "ms",
    "Russian": "ru",
    "Spanish": "es",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Vietnamese": "vi",
}


def get_language_code() -> str:
    """Get ISO 639-1 language code from TAU2_LANGUAGE env var."""
    language = os.getenv("TAU2_LANGUAGE", "").strip()
    if not language:
        return "en"
    return LANGUAGE_NAME_TO_CODE.get(language, "en")
