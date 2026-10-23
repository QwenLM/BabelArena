import os
import re
import hashlib
import json
import subprocess
from typing import Dict, Union
from datetime import datetime, timedelta
from pathlib import Path

from deepdiff import DeepDiff
from dotenv import load_dotenv
from loguru import logger
from thefuzz import fuzz, process
from json_repair import repair_json

from vita.config import DEFAULT_LANGUAGE

global_time = None

res = load_dotenv()
if not res:
    logger.warning("No .env file found")

# Data directory: VITA_DATA_DIR wins, otherwise the in-tree data/ next to the
# source. The env var lets the benchmark data live outside the source tree --
# in this distribution it is shared from the suite's top-level data/ -- which
# mirrors how tau3 resolves TAU2_DATA_DIR.
SOURCE_DIR = Path(__file__).parents[3]
_DATA_DIR_ENV = os.getenv("VITA_DATA_DIR")
DATA_DIR = Path(_DATA_DIR_ENV) if _DATA_DIR_ENV else SOURCE_DIR / "data"
if not DATA_DIR.exists():
    logger.warning(
        f"Data directory does not exist: {DATA_DIR}. "
        "Set VITA_DATA_DIR to point at the benchmark data."
    )
DOMAIN_DIR = DATA_DIR / "vita" / "domains"

TASK_FILE_SUFFIX = {
    "chinese": "",
    "english": "_en",
    "japanese": "_ja",
    "french": "_fr",
    "russian": "_ru",
    "arabic": "_ar",
    "hindi": "_hi",
    "thai": "_th",
    "spanish": "_es",
    "korean": "_ko",
    "indonesian": "_id",
    "hebrew": "_he",
    "turkish": "_tr",
    "vietnamese": "_vi",
    "malay": "_ms",
    "belarusian": "_be",
    "punjabi": "_pa",
    "kazakh": "_kk",
    "khmer": "_km",
    "burmese": "_my",
    "lao": "_lo",
    "tamil": "_ta",
    "telugu": "_te",
}

def get_task_file_path(domain: str, language: str = None) -> Path:
    """Return corresponding task file path based on language parameter"""
    if language is None:
        language = DEFAULT_LANGUAGE
    
    suffix = TASK_FILE_SUFFIX.get(language, "")
    return DOMAIN_DIR / domain / f"tasks{suffix}.json"

# Task file path definitions
DELIVERY_TASK_SET_PATH = get_task_file_path("delivery")
INSTORE_TASK_SET_PATH = get_task_file_path("instore")
CROSS_TASK_SET_PATH = get_task_file_path("cross_domain")
OTA_TASK_SET_PATH = get_task_file_path("ota")


def get_hash(obj: Union[dict, str]) -> str:
    """
    Generate a unique hash for dict.
    Returns a hex string representation of the hash.
    """
    if isinstance(obj, dict):
        hash_string = json.dumps(obj, sort_keys=True, default=str, ensure_ascii=False)
    else:
        hash_string = obj
    return hashlib.sha256(hash_string.encode()).hexdigest()


def show_dict_diff(dict1: dict, dict2: dict) -> str:
    """
    Show the difference between two dictionaries.
    """
    diff = DeepDiff(dict1, dict2)
    return diff


def get_now(format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Returns the current date and time in the format YYYYMMDD_HHMMSS.
    """
    global global_time
    if global_time is not None:
        return global_time
    now = datetime.now()
    return format_time(now, format=format)


def str_to_datetime(time: str) -> datetime:
    return datetime.strptime(time, "%Y-%m-%d %H:%M:%S")

WEEKDAY_NAMES = {
    "english": {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'},
    "japanese": {0: '月曜日', 1: '火曜日', 2: '水曜日', 3: '木曜日', 4: '金曜日', 5: '土曜日', 6: '日曜日'},
    "chinese": {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'},
    "french": {0: 'Lundi', 1: 'Mardi', 2: 'Mercredi', 3: 'Jeudi', 4: 'Vendredi', 5: 'Samedi', 6: 'Dimanche'},
    "russian": {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'},
    "arabic": {0: 'الاثنين', 1: 'الثلاثاء', 2: 'الأربعاء', 3: 'الخميس', 4: 'الجمعة', 5: 'السبت', 6: 'الأحد'},
    "hindi": {0: 'सोमवार', 1: 'मंगलवार', 2: 'बुधवार', 3: 'गुरुवार', 4: 'शुक्रवार', 5: 'शनिवार', 6: 'रविवार'},
    "thai": {0: 'วันจันทร์', 1: 'วันอังคาร', 2: 'วันพุธ', 3: 'วันพฤหัสบดี', 4: 'วันศุกร์', 5: 'วันเสาร์', 6: 'วันอาทิตย์'},
    "spanish": {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes', 5: 'Sábado', 6: 'Domingo'},
    "korean": {0: '월요일', 1: '화요일', 2: '수요일', 3: '목요일', 4: '금요일', 5: '토요일', 6: '일요일'},
    "indonesian": {0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'},
    "hebrew": {0: 'יום שני', 1: 'יום שלישי', 2: 'יום רביעי', 3: 'יום חמישי', 4: 'יום שישי', 5: 'שבת', 6: 'יום ראשון'},
    "turkish": {0: 'Pazartesi', 1: 'Salı', 2: 'Çarşamba', 3: 'Perşembe', 4: 'Cuma', 5: 'Cumartesi', 6: 'Pazar'},
    "vietnamese": {0: 'Thứ Hai', 1: 'Thứ Ba', 2: 'Thứ Tư', 3: 'Thứ Năm', 4: 'Thứ Sáu', 5: 'Thứ Bảy', 6: 'Chủ Nhật'},
    "malay": {0: 'Isnin', 1: 'Selasa', 2: 'Rabu', 3: 'Khamis', 4: 'Jumaat', 5: 'Sabtu', 6: 'Ahad'},
    "belarusian": {0: 'Панядзелак', 1: 'Аўторак', 2: 'Серада', 3: 'Чацвер', 4: 'Пятніца', 5: 'Субота', 6: 'Нядзеля'},
    "punjabi": {0: 'ਸੋਮਵਾਰ', 1: 'ਮੰਗਲਵਾਰ', 2: 'ਬੁੱਧਵਾਰ', 3: 'ਵੀਰਵਾਰ', 4: 'ਸ਼ੁੱਕਰਵਾਰ', 5: 'ਸ਼ਨਿੱਚਰਵਾਰ', 6: 'ਐਤਵਾਰ'},
    "kazakh": {0: 'Дүйсенбі', 1: 'Сейсенбі', 2: 'Сәрсенбі', 3: 'Бейсенбі', 4: 'Жұма', 5: 'Сенбі', 6: 'Жексенбі'},
    "khmer": {0: 'ច័ន្ទ', 1: 'អង្គារ', 2: 'ពុធ', 3: 'ព្រហស្បតិ៍', 4: 'សុក្រ', 5: 'សៅរ៍', 6: 'អាទិត្យ'},
    "burmese": {0: 'တနင်္လာ', 1: 'အင်္ဂါ', 2: 'ဗုဒ္ဓဟူး', 3: 'ကြာသပတေး', 4: 'သောကြာ', 5: 'စနေ', 6: 'တနင်္ဂနွေ'},
    "lao": {0: 'ວັນຈັນ', 1: 'ວັນອັງຄານ', 2: 'ວັນພຸດ', 3: 'ວັນພະຫັດ', 4: 'ວັນສຸກ', 5: 'ວັນເສົາ', 6: 'ວັນອາທິດ'},
    "tamil": {0: 'திங்கள்', 1: 'செவ்வாய்', 2: 'புதன்', 3: 'வியாழன்', 4: 'வெள்ளி', 5: 'சனி', 6: 'ஞாயிறு'},
    "telugu": {0: 'సోమవారం', 1: 'మంగళవారం', 2: 'బుధవారం', 3: 'గురువారం', 4: 'శుక్రవారం', 5: 'శనివారం', 6: 'ఆదివారం'},
}

def get_weekday(date: str, language: str = None) -> str:
    """Get weekday in the specified language"""
    if language is None:
        language = DEFAULT_LANGUAGE
    
    weekday = str_to_datetime(date).weekday()
    
    if language in WEEKDAY_NAMES:
        return WEEKDAY_NAMES[language][weekday]
    else:
        zh_dict = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}
        return f"星期{zh_dict[weekday]}"

def format_time(time: datetime, format: str = "%Y%m%d_%H%M%S") -> str:
    """
    Format the time in the format YYYYMMDD_HHMMSS.
    """
    return time.strftime(format)


def check_time_format(time: str, format="%Y-%m-%d %H:%M:%S") -> bool:
    try:
        datetime.strptime(time, format)
        return True
    except ValueError:
        return False


def check_date_format(date: str) -> bool:
    try:
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_date_between(start_date: str, end_date: str) -> list[str]:
    """
    Get Date List between start_date and end_date. (include start_date and end_date)
    """
    date_list = []
    start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
    end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
    while start_datetime < end_datetime:
        date_list.append(start_datetime.strftime("%Y-%m-%d"))
        start_datetime += timedelta(days=1)
    return date_list


def get_commit_hash() -> str:
    """
    Get the commit hash of the current directory.
    """
    try:
        commit_hash = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], text=True)
            .strip()
            .split("\n")[0]
        )
    except Exception as e:
        logger.error(f"Failed to get git hash: {e}")
        commit_hash = "unknown"
    return commit_hash


def edit_distance_score(s1: str, s2: str):
    """Calculate the edit distance between two strings."""
    dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    for i in range(len(s1) + 1):
        dp[i][0] = i
    for j in range(len(s2) + 1):
        dp[0][j] = j
    for i in range(1, len(s1) + 1):
        for j in range(1, len(s2) + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1]) + 1
    return 1 - dp[len(s1)][len(s2)] / max(len(s1), len(s2))


def rerank(keywords: str, docs: Dict[str, str], with_score: bool = False):
    # Ensure there are no duplicate values in docs
    robust_docs = {}
    val_set = set()
    for key, val in docs.items():
        while val in val_set:
            # Add a dummy suffix to the value
            val += "-"

        val_set.add(val)
        robust_docs[key] = val

    candidates = [doc for doc in robust_docs.values()]
    doc_dict_reverse = {val: key for key, val in robust_docs.items()}

    docs_sorted = process.extract(keywords, candidates, limit=None, scorer=fuzz.partial_ratio)
    if with_score:
        id_doc_sorted = [(doc_dict_reverse[doc], doc, score) for doc, score in docs_sorted]
    else:
        id_doc_sorted = [(doc_dict_reverse[doc], doc) for doc, _ in docs_sorted]

    return id_doc_sorted


def fuzzy_match(x: str, y: str) -> bool:
    if fuzz.partial_ratio(x, y) >= 40:
        return True
    else:
        return False


def fuzzy_ratio_match(x: str, y: str) -> bool:
    if fuzz.ratio(x, y) >= 20:
        return True
    else:
        return False


def json_check(json_str: str) -> bool:
    try:
        json.loads(json_str)
        return True
    except (ValueError, json.JSONDecodeError) as e:
        print(f"Format error: {e}")
        return False


def extract_json_fields(json_str):
    """Simple function to extract JSON fields"""
    rubrics_pattern = r'"rubrics":\s*"(.*?)"(?=,|\s*})'
    reasoning_pattern = r'"reasoning":\s*"(.*?)"(?=,|\s*})'
    meet_expectation_pattern = r'"meetExpectation":\s*(true|false)'

    rubrics_list = re.findall(rubrics_pattern, json_str, re.DOTALL)
    reasoning_list = re.findall(reasoning_pattern, json_str, re.DOTALL)
    meet_expectation_list = re.findall(meet_expectation_pattern, json_str)

    results = []
    max_length = max(len(rubrics_list), len(reasoning_list), len(meet_expectation_list))

    for i in range(max_length):
        obj_result = {}
        if i < len(rubrics_list):
            obj_result['rubrics'] = rubrics_list[i]
        if i < len(reasoning_list):
            obj_result['reasoning'] = reasoning_list[i]
        if i < len(meet_expectation_list):
            obj_result['meetExpectation'] = meet_expectation_list[i] == 'true'

        results.append(obj_result)

    return results


def evaluator_extracter(content: str) -> list[dict]:
    """
    Extract the result from the content.
    """
    good_json_string = repair_json(content)
    result_data = json.loads(good_json_string)
    return result_data
