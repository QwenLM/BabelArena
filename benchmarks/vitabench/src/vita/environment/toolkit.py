import math
import logging
import holidays
from enum import Enum
from typing import Annotated, Any, Callable, Dict, Optional, TypeVar
from functools import wraps
from datetime import datetime
from pydantic import BaseModel, Field
from thefuzz import process, fuzz

from vita.environment.db import DB
from vita.environment.tool import Tool, as_tool
from vita.utils import get_hash, update_pydantic_model_with_dict, get_now
from vita.utils.utils import rerank, fuzzy_ratio_match, check_time_format
from vita.data_model.tasks import Location

TOOL_ATTR = "__tool__"
TOOL_TYPE_ATTR = "__tool_type__"

_CN_TO_JA_HOLIDAY_NAMES = {
    "元旦": "元日",
    "春节": "春節",
    "清明节": "清明節",
    "劳动节": "メーデー",
    "端午节": "端午節",
    "中秋节": "中秋節",
    "国庆节": "国慶節",
}

_CN_TO_EN_HOLIDAY_NAMES = {
    "元旦": "New Year's Day",
    "春节": "Spring Festival",
    "清明节": "Qingming Festival",
    "劳动节": "Labor Day",
    "端午节": "Dragon Boat Festival",
    "中秋节": "Mid-Autumn Festival",
    "国庆节": "National Day",
}

_CN_TO_FR_HOLIDAY_NAMES = {
    "元旦节": "Jour de l'an",
    "立秋": "Début de l'automne",
    "妇女节": "Journée internationale des femmes",
    "腊八节": "Fête de Laba",
    "龙头节": "Fête du dragon",
    "建党节": "Fondation du Parti",
    "清明节": "Fête de Qingming",
    "重阳节": "Fête de Chongyang",
    "端午节": "Fête du Dragon",
    "母亲节": "Fête des Mères",
    "元宵节": "Fête des Lanternes",
    "劳动节": "Fête du Travail",
    "七夕节": "Fête de Qixi",
    "冬至": "Solstice d'hiver",
    "圣诞节": "Noël",
    "国庆节": "Fête nationale",
    "中秋节": "Fête de la Mi-Automne",
    "情人节": "Saint-Valentin",
    "父亲节": "Fête des Pères",
}

_CN_TO_RU_HOLIDAY_NAMES = {
    "元旦节": "Новый год",
    "立秋": "Начало осени",
    "妇女节": "Международный женский день",
    "腊八节": "Фестиваль Лаба",
    "龙头节": "Фестиваль Дракона",
    "建党节": "День основания партии",
    "清明节": "Фестиваль Цинмин",
    "重阳节": "Фестиваль Чунъян",
    "端午节": "Фестиваль лодок-драконов",
    "母亲节": "День матери",
    "元宵节": "Фестиваль фонарей",
    "劳动节": "День труда",
    "七夕节": "Фестиваль Циси",
    "冬至": "Зимнее солнцестояние",
    "圣诞节": "Рождество",
    "国庆节": "Национальный день",
    "中秋节": "Фестиваль середины осени",
    "情人节": "День святого Валентина",
    "父亲节": "День отца",
}

_CN_TO_AR_HOLIDAY_NAMES = {
    "元旦节": "رأس السنة",
    "立秋": "بداية الخريف",
    "妇女节": "اليوم العالمي للمرأة",
    "腊八节": "مهرجان لابا",
    "龙头节": "مهرجان التنين",
    "建党节": "يوم تأسيس الحزب",
    "清明节": "مهرجان تشينغ مينغ",
    "重阳节": "مهرجان تشونغ يانغ",
    "端午节": "مهرجان قوارب التنين",
    "母亲节": "عيد الأم",
    "元宵节": "مهرجان المصابيح",
    "劳动节": "عيد العمال",
    "七夕节": "مهرجان تشي شي",
    "冬至": "الانقلاب الشتوي",
    "圣诞节": "عيد الميلاد",
    "国庆节": "اليوم الوطني",
    "中秋节": "مهرجان منتصف الخريف",
    "情人节": "عيد الحب",
    "父亲节": "عيد الأب",
}

_CN_TO_HI_HOLIDAY_NAMES = {
    "元旦节": "नया साल",
    "立秋": "शरद ऋतु की शुरुआत",
    "妇女节": "अंतर्राष्ट्रीय महिला दिवस",
    "腊八节": "लाबा महोत्सव",
    "龙头节": "ड्रैगन महोत्सव",
    "建党节": "पार्टी स्थापना दिवस",
    "清明节": "चिंगमिंग महोत्सव",
    "重阳节": "चुंगयांग महोत्सव",
    "端午节": "ड्रैगन बोट महोत्सव",
    "母亲节": "मातृ दिवस",
    "元宵节": "लालटेन महोत्सव",
    "劳动节": "श्रम दिवस",
    "七夕节": "किसी महोत्सव",
    "冬至": "शीत संक्रांति",
    "圣诞节": "क्रिसमस",
    "国庆节": "राष्ट्रीय दिवस",
    "中秋节": "मध्य शरद महोत्सव",
    "情人节": "वैलेंटाइन दिवस",
    "父亲节": "पिता दिवस",
}

_CN_TO_TH_HOLIDAY_NAMES = {
    "元旦节": "วันขึ้นปีใหม่",
    "立秋": "เริ่มฤดูใบไม้ร่วง",
    "妇女节": "วันสตรีสากล",
    "腊八节": "เทศกาลลาปา",
    "龙头节": "เทศกาลมังกร",
    "建党节": "วันก่อตั้งพรรค",
    "清明节": "เทศกาลชิงหมิง",
    "重阳节": "เทศกาลฉงหยาง",
    "端午节": "เทศกาลเรือมังกร",
    "母亲节": "วันแม่",
    "元宵节": "เทศกาลโคมไฟ",
    "劳动节": "วันแรงงาน",
    "七夕节": "เทศกาลชีซี",
    "冬至": "เหมายัน",
    "圣诞节": "คริสต์มาส",
    "国庆节": "วันชาติ",
    "中秋节": "เทศกาลกลางฤดูใบไม้ร่วง",
    "情人节": "วันวาเลนไทน์",
    "父亲节": "วันพ่อ",
}

_CN_TO_ES_HOLIDAY_NAMES = {
    "元旦节": "Año Nuevo",
    "立秋": "Inicio del otoño",
    "妇女节": "Día Internacional de la Mujer",
    "腊八节": "Festival de Laba",
    "龙头节": "Festival del Dragón",
    "建党节": "Día de la Fundación del Partido",
    "清明节": "Festival de Qingming",
    "重阳节": "Festival de Chongyang",
    "端午节": "Festival del Barco Dragón",
    "母亲节": "Día de la Madre",
    "元宵节": "Festival de los Faroles",
    "劳动节": "Día del Trabajo",
    "七夕节": "Festival de Qixi",
    "冬至": "Solsticio de invierno",
    "圣诞节": "Navidad",
    "国庆节": "Día Nacional",
    "中秋节": "Festival de Medio Otoño",
    "情人节": "Día de San Valentín",
    "父亲节": "Día del Padre",
}

_CN_TO_KO_HOLIDAY_NAMES = {
    "元旦节": "새해", "立秋": "입추", "妇女节": "세계 여성의 날",
    "腊八节": "라바절", "龙头节": "용머리절", "建党节": "당 창건 기념일",
    "清明节": "청명절", "重阳节": "중양절", "端午节": "단오절",
    "母亲节": "어머니날", "元宵节": "정월 대보름", "劳动节": "노동절",
    "七夕节": "칠석", "冬至": "동지", "圣诞节": "크리스마스",
    "国庆节": "국경절", "中秋节": "중추절", "情人节": "발렌타인데이", "父亲节": "아버지날",
}

_CN_TO_ID_HOLIDAY_NAMES = {
    "元旦节": "Tahun Baru", "立秋": "Awal Musim Gugur", "妇女节": "Hari Perempuan Internasional",
    "腊八节": "Festival Laba", "龙头节": "Festival Naga", "建党节": "Hari Pendirian Partai",
    "清明节": "Festival Qingming", "重阳节": "Festival Chongyang", "端午节": "Festival Perahu Naga",
    "母亲节": "Hari Ibu", "元宵节": "Festival Lampion", "劳动节": "Hari Buruh",
    "七夕节": "Festival Qixi", "冬至": "Titik Balik Matahari Musim Dingin", "圣诞节": "Natal",
    "国庆节": "Hari Nasional", "中秋节": "Festival Pertengahan Musim Gugur", "情人节": "Hari Valentine", "父亲节": "Hari Ayah",
}

_CN_TO_HE_HOLIDAY_NAMES = {
    "元旦节": "ראש השנה האזרחית", "立秋": "תחילת הסתיו", "妇女节": "יום האישה הבינלאומי",
    "腊八节": "פסטיבל לאבא", "龙头节": "פסטיבל הדרקון", "建党节": "יום ייסוד המפלגה",
    "清明节": "פסטיבל צ'ינגמינג", "重阳节": "פסטיבל צ'ונגיאנג", "端午节": "פסטיבל סירות הדרקון",
    "母亲节": "יום האם", "元宵节": "פסטיבל הפנסים", "劳动节": "יום העבודה",
    "七夕节": "פסטיבל צ'יסי", "冬至": "היפוך החורף", "圣诞节": "חג המולד",
    "国庆节": "היום הלאומי", "中秋节": "פסטיבל אמצע הסתיו", "情人节": "יום האהבה", "父亲节": "יום האב",
}

_CN_TO_TR_HOLIDAY_NAMES = {
    "元旦节": "Yılbaşı", "立秋": "Sonbahar Başlangıcı", "妇女节": "Dünya Kadınlar Günü",
    "腊八节": "Laba Festivali", "龙头节": "Ejderha Festivali", "建党节": "Parti Kuruluş Günü",
    "清明节": "Qingming Festivali", "重阳节": "Chongyang Festivali", "端午节": "Ejderha Teknesi Festivali",
    "母亲节": "Anneler Günü", "元宵节": "Fener Festivali", "劳动节": "İşçi Bayramı",
    "七夕节": "Qixi Festivali", "冬至": "Kış Gündönümü", "圣诞节": "Noel",
    "国庆节": "Ulusal Gün", "中秋节": "Sonbahar Ortası Festivali", "情人节": "Sevgililer Günü", "父亲节": "Babalar Günü",
}

_CN_TO_VI_HOLIDAY_NAMES = {
    "元旦节": "Tết Dương lịch", "立秋": "Lập Thu", "妇女节": "Ngày Quốc tế Phụ nữ",
    "腊八节": "Lễ hội Lạp Bát", "龙头节": "Lễ hội Rồng", "建党节": "Ngày thành lập Đảng",
    "清明节": "Tết Thanh Minh", "重阳节": "Tết Trùng Dương", "端午节": "Tết Đoan Ngọ",
    "母亲节": "Ngày của Mẹ", "元宵节": "Tết Nguyên Tiêu", "劳动节": "Ngày Quốc tế Lao động",
    "七夕节": "Lễ hội Thất Tịch", "冬至": "Đông Chí", "圣诞节": "Giáng Sinh",
    "国庆节": "Quốc Khánh", "中秋节": "Tết Trung Thu", "情人节": "Ngày lễ Tình nhân", "父亲节": "Ngày của Cha",
}

_CN_TO_MS_HOLIDAY_NAMES = {
    "元旦节": "Tahun Baharu", "立秋": "Permulaan Musim Luruh", "妇女节": "Hari Wanita Antarabangsa",
    "腊八节": "Perayaan Laba", "龙头节": "Perayaan Naga", "建党节": "Hari Penubuhan Parti",
    "清明节": "Perayaan Qingming", "重阳节": "Perayaan Chongyang", "端午节": "Perayaan Bot Naga",
    "母亲节": "Hari Ibu", "元宵节": "Perayaan Tanglung", "劳动节": "Hari Pekerja",
    "七夕节": "Perayaan Qixi", "冬至": "Solstis Musim Sejuk", "圣诞节": "Krismas",
    "国庆节": "Hari Kebangsaan", "中秋节": "Perayaan Pertengahan Musim Luruh", "情人节": "Hari Kekasih", "父亲节": "Hari Bapa",
}

_CN_TO_BE_HOLIDAY_NAMES = {
    "元旦节": "Новы год", "立秋": "Пачатак восені", "妇女节": "Міжнародны жаночы дзень",
    "腊八节": "Фестываль Лаба", "龙头节": "Фестываль Дракона", "建党节": "Дзень заснавання партыі",
    "清明节": "Фестываль Цінмін", "重阳节": "Фестываль Чунъян", "端午节": "Фестываль лодак-драконаў",
    "母亲节": "Дзень маці", "元宵节": "Фестываль ліхтароў", "劳动节": "Дзень працы",
    "七夕节": "Фестываль Цісі", "冬至": "Зімовае сонцастаянне", "圣诞节": "Каляды",
    "国庆节": "Нацыянальны дзень", "中秋节": "Фестываль сярэдзіны восені", "情人节": "Дзень закаханых", "父亲节": "Дзень бацькі",
}

_CN_TO_PA_HOLIDAY_NAMES = {
    "元旦节": "ਨਵਾਂ ਸਾਲ", "立秋": "ਪਤਝੜ ਦੀ ਸ਼ੁਰੂਆਤ", "妇女节": "ਅੰਤਰਰਾਸ਼ਟਰੀ ਮਹਿਲਾ ਦਿਵਸ",
    "腊八节": "ਲਾਬਾ ਤਿਉਹਾਰ", "龙头节": "ਡ੍ਰੈਗਨ ਤਿਉਹਾਰ", "建党节": "ਪਾਰਟੀ ਸਥਾਪਨਾ ਦਿਵਸ",
    "清明节": "ਚਿੰਗਮਿੰਗ ਤਿਉਹਾਰ", "重阳节": "ਚੁੰਗਯਾਂਗ ਤਿਉਹਾਰ", "端午节": "ਡ੍ਰੈਗਨ ਬੋਟ ਤਿਉਹਾਰ",
    "母亲节": "ਮਾਂ ਦਿਵਸ", "元宵节": "ਲਾਲਟੈਣ ਤਿਉਹਾਰ", "劳动节": "ਮਜ਼ਦੂਰ ਦਿਵਸ",
    "七夕节": "ਕਿਸੀ ਤਿਉਹਾਰ", "冬至": "ਸਰਦੀ ਸੰਕ੍ਰਾਂਤੀ", "圣诞节": "ਕ੍ਰਿਸਮਸ",
    "国庆节": "ਰਾਸ਼ਟਰੀ ਦਿਵਸ", "中秋节": "ਮੱਧ ਪਤਝੜ ਤਿਉਹਾਰ", "情人节": "ਵੈਲੇਨਟਾਈਨ ਦਿਵਸ", "父亲节": "ਪਿਤਾ ਦਿਵਸ",
}

_CN_TO_KK_HOLIDAY_NAMES = {
    "元旦节": "Жаңа жыл", "立秋": "Күздің басталуы", "妇女节": "Халықаралық әйелдер күні",
    "腊八节": "Лаба мейрамы", "龙头节": "Айдаһар мейрамы", "建党节": "Партия құру күні",
    "清明节": "Цинмин мейрамы", "重阳节": "Чунъян мейрамы", "端午节": "Айдаһар қайығы мейрамы",
    "母亲节": "Аналар күні", "元宵节": "Шам мейрамы", "劳动节": "Еңбек күні",
    "七夕节": "Циси мейрамы", "冬至": "Қысқы күн тоқырауы", "圣诞节": "Рождество",
    "国庆节": "Ұлттық күн", "中秋节": "Күз ортасы мейрамы", "情人节": "Ғашықтар күні", "父亲节": "Әкелер күні",
}

_CN_TO_KM_HOLIDAY_NAMES = {
    "元旦节": "ចូលឆ្នាំថ្មី", "立秋": "ចូលរដូវស្លឹកឈើជ្រុះ", "妇女节": "ទិវានារីអន្តរជាតិ",
    "腊八节": "ពិធីបុណ្យឡាបា", "龙头节": "ពិធីបុណ្យនាគ", "建党节": "ទិវាបង្កើតបក្ស",
    "清明节": "ពិធីបុណ្យឈីងមីង", "重阳节": "ពិធីបុណ្យចុងយ៉ាង", "端午节": "ពិធីបុណ្យទូកនាគ",
    "母亲节": "ទិវាម្តាយ", "元宵节": "ពិធីបុណ្យភ្លើងពណ៌", "劳动节": "ទិវាពលកម្ម",
    "七夕节": "ពិធីបុណ្យឈីស៊ី", "冬至": "រដូវរងាសុរិយវិថី", "圣诞节": "ណូអែល",
    "国庆节": "ទិវាជាតិ", "中秋节": "ពិធីបុណ្យពាក់កណ្តាលរដូវស្លឹកឈើជ្រុះ", "情人节": "ទិវាបុណ្យនៃក្ដីស្រឡាញ់", "父亲节": "ទិវាឪពុក",
}

_CN_TO_MY_HOLIDAY_NAMES = {
    "元旦节": "နှစ်သစ်ကူး", "立秋": "ဆောင်းဦးစချိန်", "妇女节": "အပြည်ပြည်ဆိုင်ရာအမျိုးသမီးများနေ့",
    "腊八节": "လာဗာပွဲတော်", "龙头节": "နဂါးပွဲတော်", "建党节": "ပါတီတည်ထောင်သည့်နေ့",
    "清明节": "ချင်မင်းပွဲတော်", "重阳节": "ချုံယန်ပွဲတော်", "端午节": "နဂါးလှေပွဲတော်",
    "母亲节": "မိခင်များနေ့", "元宵节": "မီးပုံးပွဲတော်", "劳动节": "အလုပ်သမားနေ့",
    "七夕节": "ချီရှီပွဲတော်", "冬至": "ဆောင်းရာသီနေ့တိုဆုံးအချိန်", "圣诞节": "ခရစ္စမတ်",
    "国庆节": "အမျိုးသားနေ့", "中秋节": "ဆောင်းဦးလယ်ပွဲတော်", "情人节": "ချစ်သူများနေ့", "父亲节": "ဖခင်များနေ့",
}

_CN_TO_LO_HOLIDAY_NAMES = {
    "元旦节": "ປີໃໝ່", "立秋": "ເລີ່ມລະດູໃບໄມ້ຫຼົ່ນ", "妇女节": "ວັນແມ່ຍິງສາກົນ",
    "腊八节": "ບຸນລາບາ", "龙头节": "ບຸນມັງກອນ", "建党节": "ວັນສ້າງຕັ້ງພັກ",
    "清明节": "ບຸນຊິງມິງ", "重阳节": "ບຸນຊົງຢ່າງ", "端午节": "ບຸນເຮືອມັງກອນ",
    "母亲节": "ວັນແມ່", "元宵节": "ບຸນໂຄມໄຟ", "劳动节": "ວັນແຮງງານ",
    "七夕节": "ບຸນຊີຊີ", "冬至": "ວັນເຫມາຍັນ", "圣诞节": "ຄຣິສມາສ",
    "国庆节": "ວັນຊາດ", "中秋节": "ບຸນກາງລະດູໃບໄມ້ຫຼົ່ນ", "情人节": "ວັນວາເລນທາຍ", "父亲节": "ວັນພໍ່",
}

_CN_TO_TA_HOLIDAY_NAMES = {
    "元旦节": "புத்தாண்டு", "立秋": "இலையுதிர் காலத் தொடக்கம்", "妇女节": "சர்வதேச மகளிர் தினம்",
    "腊八节": "லாபா திருவிழா", "龙头节": "டிராகன் திருவிழா", "建党节": "கட்சி நிறுவிய நாள்",
    "清明节": "சிங்மிங் திருவிழா", "重阳节": "சொங்யாங் திருவிழா", "端午节": "டிராகன் படகு திருவிழா",
    "母亲节": "தாய் தினம்", "元宵节": "விளக்கு திருவிழா", "劳动节": "தொழிலாளர் தினம்",
    "七夕节": "சீசி திருவிழா", "冬至": "குளிர்கால சங்கிராந்தி", "圣诞节": "கிறிஸ்துமஸ்",
    "国庆节": "தேசிய தினம்", "中秋节": "நடு இலையுதிர் திருவிழா", "情人节": "காதலர் தினம்", "父亲节": "தந்தையர் தினம்",
}

_CN_TO_TE_HOLIDAY_NAMES = {
    "元旦节": "నూతన సంవత్సరం", "立秋": "శరదృతువు ప్రారంభం", "妇女节": "అంతర్జాతీయ మహిళా దినోత్సవం",
    "腊八节": "లాబా పండుగ", "龙头节": "డ్రాగన్ పండుగ", "建党节": "పార్టీ స్థాపన దినం",
    "清明节": "చింగ్‌మింగ్ పండుగ", "重阳节": "చుంగ్‌యాంగ్ పండుగ", "端午节": "డ్రాగన్ బోట్ పండుగ",
    "母亲节": "మాతృ దినోత్సవం", "元宵节": "దీపోత్సవం", "劳动节": "కార్మిక దినోత్సవం",
    "七夕节": "చీసీ పండుగ", "冬至": "ఉత్తరాయణ సంక్రాంతి", "圣诞节": "క్రిస్మస్",
    "国庆节": "జాతీయ దినోత్సవం", "中秋节": "మధ్య శరదృతు పండుగ", "情人节": "వాలెంటైన్స్ డే", "父亲节": "తండ్రుల దినోత్సవం",
}

T = TypeVar("T", bound=DB)


class ToolKitType(type):
    """Metaclass for ToolKit classes."""

    def __init__(cls, name, bases, attrs):
        func_tools = {}
        
        # Import schema utilities
        from vita.environment.toolkit_schema import get_domain_from_class, generate_tool_docstring
        
        # Import delivery schema to ensure it's available
        try:
            from vita.domains.delivery.tools_schema import TOOL_DESCRIPTIONS
        except ImportError:
            pass
        
        # Import instore schema to ensure it's available
        try:
            from vita.domains.instore.tools_schema import TOOL_DESCRIPTIONS
        except ImportError:
            pass
        
        # Import ota schema to ensure it's available
        try:
            from vita.domains.ota.tools_schema import TOOL_DESCRIPTIONS
        except ImportError:
            pass
        
        # Determine domain for this class
        domain = get_domain_from_class(cls)
        
        for name, method in attrs.items():
            if isinstance(method, property):
                method = method.fget
            if hasattr(method, TOOL_ATTR):
                # Try to enhance the docstring if we have domain information
                if domain:
                    # Use the method name directly since it's the same as the tool name
                    tool_name = name
                    try:
                        # Use current global language setting
                        from vita.utils.schema_utils import get_global_language
                        current_language = get_global_language()
                        enhanced_docstring = generate_tool_docstring(domain, tool_name, current_language)
                        if enhanced_docstring:
                            # Update the method's docstring
                            method.__doc__ = enhanced_docstring
                    except Exception:
                        # If schema lookup fails, keep the original docstring
                        pass
                
                func_tools[name] = method

        @property
        def _func_tools(self) -> Dict[str, Callable]:
            """Get the tools available in the ToolKit."""
            all_func_tools = func_tools.copy()
            try:
                all_func_tools.update(super(cls, self)._func_tools)
            except AttributeError:
                pass

            try:
                for attr_name in object.__getattribute__(self, '__dict__'):
                    if not attr_name.startswith("__"):
                        try:
                            attr = object.__getattribute__(self, attr_name)
                            if callable(attr) and hasattr(attr, TOOL_ATTR) and attr_name not in all_func_tools:
                                # Try to enhance the docstring for dynamically added tools too
                                if domain:
                                    # Use the attribute name directly since it's the same as the tool name
                                    tool_name = attr_name
                                    try:
                                        # Use current global language setting
                                        from vita.utils.schema_utils import get_global_language
                                        current_language = get_global_language()
                                        enhanced_docstring = generate_tool_docstring(domain, tool_name, current_language)
                                        if enhanced_docstring:
                                            attr.__doc__ = enhanced_docstring
                                    except Exception:
                                        pass
                                
                                all_func_tools[attr_name] = attr
                        except AttributeError:
                            continue
            except AttributeError:
                pass

            return all_func_tools

        cls._func_tools = _func_tools


class ToolType(str, Enum):
    """Type of a tool."""

    READ = "read"
    WRITE = "write"
    THINK = "think"
    GENERIC = "generic"


def is_tool(tool_type: ToolType = ToolType.READ, domain: str = None, tool_name: str = None):
    """Decorator to mark a function as a tool.

    Args:
        tool_type: The type of the tool (READ, WRITE, THINK, GENERIC)
        domain: The domain name for schema lookup (optional)
        tool_name: The tool name for schema lookup (optional, defaults to function name)
    """

    def decorator(func):
        # Try to get domain from the class if not provided
        if domain is None:
            # This will be set when the decorator is applied to a method
            # We'll handle it in the metaclass
            pass
        
        # Try to get tool name if not provided
        actual_tool_name = tool_name or func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except AssertionError as e:
                return str(e)

        setattr(wrapper, TOOL_ATTR, True)
        setattr(wrapper, TOOL_TYPE_ATTR, tool_type)
        
        # Store additional metadata for schema lookup
        setattr(wrapper, "__tool_domain__", domain)
        setattr(wrapper, "__tool_name__", actual_tool_name)
        
        return wrapper

    return decorator


class ToolKitBase(metaclass=ToolKitType):
    """Base class for ToolKit classes."""

    def __init__(self, db: Optional[T] = None):
        self.db: Optional[T] = db
        self._update_tool_descriptions()

    @property
    def tools(self) -> Dict[str, Callable]:
        """Get the tools available in the ToolKit."""
        return {name: getattr(self, name) for name in self._func_tools.keys()}

    def use_tool(self, tool_name: str, **kwargs) -> str:
        """Use a tool."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found.")
        return self.tools[tool_name](**kwargs)

    def _update_tool_descriptions(self):
        try:
            from vita.utils.schema_utils import get_global_language, generate_tool_docstring
            from vita.environment.toolkit_schema import get_domain_from_class

            current_language = get_global_language()
            domain = get_domain_from_class(self.__class__)

            toolkit_domain = get_domain_from_class(ToolKitBase)

            if domain:
                for tool_name in self._func_tools.keys():
                    try:
                        enhanced_docstring = generate_tool_docstring(domain, tool_name, current_language)

                        if not enhanced_docstring and toolkit_domain:
                            enhanced_docstring = generate_tool_docstring(toolkit_domain, tool_name, current_language)

                        if enhanced_docstring:
                            tool_func = getattr(self, tool_name)
                            if hasattr(tool_func, '__doc__'):
                                if hasattr(tool_func, '__func__'):
                                    tool_func.__func__.__doc__ = enhanced_docstring
                                else:
                                    tool_func.__doc__ = enhanced_docstring
                    except Exception as e:
                        logging.debug(f"Failed to update docstring for {tool_name}: {e}")
        except Exception as e:
            logging.debug(f"Failed to update tool descriptions: {e}")

    def get_tools(self) -> Dict[str, Tool]:
        """Get the tools available in the ToolKit.
        Uses the `as_tool` to convert the functions to Tool objects.

        Returns:
            A dictionary of tools available in the ToolKit.
        """
        self._update_tool_descriptions()

        logging.debug(f"TOOLKIT: self.tools.items() {self.tools.items()}")
        return {name: as_tool(tool) for name, tool in self.tools.items()}

    def has_tool(self, tool_name: str) -> bool:
        """Check if a tool exists in the ToolKit."""
        return tool_name in self.tools

    def tool_type(self, tool_name: str) -> ToolType:
        """Get the type of a tool."""
        tool = self.tools[tool_name]
        return getattr(tool, TOOL_TYPE_ATTR, ToolType.GENERIC)

    def get_statistics(self) -> dict[str, Any]:
        """Get the statistics of the ToolKit."""
        num_tools = len(self.tools)
        num_read_tools = sum(
            self.tool_type(name) == ToolType.READ for name in self.tools
        )
        num_write_tools = sum(
            self.tool_type(name) == ToolType.WRITE for name in self.tools
        )
        num_think_tools = sum(
            self.tool_type(name) == ToolType.THINK for name in self.tools
        )
        num_generic_tools = sum(
            self.tool_type(name) == ToolType.GENERIC for name in self.tools
        )
        return {
            "num_tools": num_tools,
            "num_read_tools": num_read_tools,
            "num_write_tools": num_write_tools,
            "num_think_tools": num_think_tools,
            "num_generic_tools": num_generic_tools,
        }

    def update_db(self, update_data: Optional[dict[str, Any]] = None):
        """Update the database of the ToolKit."""
        if update_data is None:
            update_data = {}
        if self.db is None:
            raise ValueError("Database has not been initialized.")
        self.db = update_pydantic_model_with_dict(self.db, update_data)

    def get_db_hash(self) -> str:
        """Get the hash of the database."""
        return get_hash(self.db.model_dump())

    @is_tool(ToolType.GENERIC)
    def longitude_latitude_to_distance(self, longitude1: float, latitude1: float, longitude2: float,
                                       latitude2: float) -> float:
        if longitude1 == longitude2 and latitude1 == latitude2:
            return 0.0

        R = 6371000
        lon1, lat1, lon2, lat2 = map(math.radians, [longitude1, latitude1, longitude2, latitude2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        return round(distance, 0)

    @is_tool(ToolType.GENERIC)
    def weather(self, address: str, date_start: str, date_end: str) -> str:
        assert check_time_format(date_start,
                                 "%Y-%m-%d"), f"Invalid date_start format. Expected yyyy-mm-dd, got: {date_start}"
        assert check_time_format(date_end, "%Y-%m-%d"), f"Invalid date_end format. Expected yyyy-mm-dd, got: {date_end}"

        assert address and address.strip(), "Address cannot be empty"
        weather_dict = {city_weather.city: city_weather for city_weather in self.db.weather}
        weather_dict_for_rerank = {city_weather.city: city_weather.city for city_weather in self.db.weather}
        weather_info = rerank(address, weather_dict_for_rerank, True)[0]
        if weather_info[-1] < 50:
            raise ValueError(f"Weather information not found for {address}")

        filtered_weather = []
        start_date = datetime.strptime(date_start, "%Y-%m-%d").date()
        end_date = datetime.strptime(date_end, "%Y-%m-%d").date()
        for city_weather in self.db.weather:
            if city_weather.city == weather_info[0]:
                weather_date = datetime.strptime(city_weather.datetime, "%Y-%m-%d").date()
                if start_date <= weather_date <= end_date:
                    filtered_weather.append(city_weather)

        if filtered_weather:
            filtered_weather.sort(key=lambda x: x.datetime)
            weather_results = []
            for weather in filtered_weather:
                weather_results.append(repr(weather))
            return "\n".join(weather_results)
        else:
            return f"No weather information found for {weather_info[0]} between {date_start} and {date_end}"

    @is_tool(ToolType.GENERIC)
    def address_to_longitude_latitude(self, address: str) -> tuple[float, float]:
        assert address and address.strip(), "Address cannot be empty"
        address_lng_lat_dict = Location.get_all()
        address_lng_lat_dict_for_rerank = {address: address for address in address_lng_lat_dict.keys()}
        address_info = rerank(address, address_lng_lat_dict_for_rerank, True)[0]
        if address_info[-1] < 30 or not fuzzy_ratio_match(address, address_info[0]):
            raise ValueError(f"Longitude and latitude not found for address {address}")
        address_lng_lat = address_lng_lat_dict.get(address_info[0])
        return [address_lng_lat.longitude, address_lng_lat.latitude]

    @is_tool(ToolType.GENERIC)
    def get_date_holiday_info(self, date: str) -> str:
        assert check_time_format(date, "%Y-%m-%d"), f"Date format error, should be yyyy-mm-dd, actual: {date}"
        date_format = datetime.strptime(date, "%Y-%m-%d")
        cn = holidays.China(years=date_format.year)
        holiday_name = cn.get(date_format)
        if holiday_name is None:
            return f"Date {date} is not a holiday"

        from vita.utils.schema_utils import get_global_language
        current_language = get_global_language()
        _HOLIDAY_NAME_MAPS = {
            'japanese': _CN_TO_JA_HOLIDAY_NAMES, 'english': _CN_TO_EN_HOLIDAY_NAMES,
            'french': _CN_TO_FR_HOLIDAY_NAMES, 'russian': _CN_TO_RU_HOLIDAY_NAMES,
            'arabic': _CN_TO_AR_HOLIDAY_NAMES, 'hindi': _CN_TO_HI_HOLIDAY_NAMES,
            'thai': _CN_TO_TH_HOLIDAY_NAMES, 'spanish': _CN_TO_ES_HOLIDAY_NAMES,
            'korean': _CN_TO_KO_HOLIDAY_NAMES, 'indonesian': _CN_TO_ID_HOLIDAY_NAMES,
            'hebrew': _CN_TO_HE_HOLIDAY_NAMES, 'turkish': _CN_TO_TR_HOLIDAY_NAMES,
            'vietnamese': _CN_TO_VI_HOLIDAY_NAMES, 'malay': _CN_TO_MS_HOLIDAY_NAMES,
            'belarusian': _CN_TO_BE_HOLIDAY_NAMES, 'punjabi': _CN_TO_PA_HOLIDAY_NAMES,
            'kazakh': _CN_TO_KK_HOLIDAY_NAMES, 'khmer': _CN_TO_KM_HOLIDAY_NAMES,
            'burmese': _CN_TO_MY_HOLIDAY_NAMES, 'lao': _CN_TO_LO_HOLIDAY_NAMES,
            'tamil': _CN_TO_TA_HOLIDAY_NAMES, 'telugu': _CN_TO_TE_HOLIDAY_NAMES,
        }
        name_map = _HOLIDAY_NAME_MAPS.get(current_language)
        if name_map:
            holiday_name = name_map.get(holiday_name, holiday_name)

        return holiday_name

    @is_tool(ToolType.GENERIC)
    def get_holiday_date(self, year: str, holiday_name: str) -> str:
        from vita.utils.schema_utils import get_global_language

        current_language = get_global_language()

        # Base holiday data in Chinese — dates are language-independent
        _cn_holiday_data = {
            "2025": {
                "元旦节": "2025-01-01", "立秋": "2025-08-07", "妇女节": "2025-03-08",
                "腊八节": "2025-01-07", "龙头节": "2025-03-01", "建党节": "2025-07-01",
                "清明节": "2025-04-04", "重阳节": "2025-10-29", "端午节": "2025-05-31",
                "母亲节": "2025-05-11", "元宵节": "2025-02-15", "劳动节": "2025-05-01",
                "七夕节": "2025-08-29", "冬至": "2025-12-21", "圣诞节": "2025-12-25",
                "国庆节": "2025-10-01", "中秋节": "2025-10-06",
            },
            "2024": {
                "重阳节": "2024-10-11", "七夕节": "2024-08-10", "情人节": "2024-02-14",
                "清明节": "2024-04-04", "端午节": "2024-06-10", "元宵节": "2024-02-24",
                "中秋节": "2024-09-17",
            },
            "2023": {
                "国庆节": "2023-10-01", "端午节": "2023-06-22", "中秋节": "2023-09-29",
                "清明节": "2023-04-05", "重阳节": "2023-10-23", "父亲节": "2023-06-18",
            },
        }

        _holiday_name_maps = {
            'japanese': _CN_TO_JA_HOLIDAY_NAMES, 'english': _CN_TO_EN_HOLIDAY_NAMES,
            'french': _CN_TO_FR_HOLIDAY_NAMES, 'russian': _CN_TO_RU_HOLIDAY_NAMES,
            'arabic': _CN_TO_AR_HOLIDAY_NAMES, 'hindi': _CN_TO_HI_HOLIDAY_NAMES,
            'thai': _CN_TO_TH_HOLIDAY_NAMES, 'spanish': _CN_TO_ES_HOLIDAY_NAMES,
            'korean': _CN_TO_KO_HOLIDAY_NAMES, 'indonesian': _CN_TO_ID_HOLIDAY_NAMES,
            'hebrew': _CN_TO_HE_HOLIDAY_NAMES, 'turkish': _CN_TO_TR_HOLIDAY_NAMES,
            'vietnamese': _CN_TO_VI_HOLIDAY_NAMES, 'malay': _CN_TO_MS_HOLIDAY_NAMES,
            'belarusian': _CN_TO_BE_HOLIDAY_NAMES, 'punjabi': _CN_TO_PA_HOLIDAY_NAMES,
            'kazakh': _CN_TO_KK_HOLIDAY_NAMES, 'khmer': _CN_TO_KM_HOLIDAY_NAMES,
            'burmese': _CN_TO_MY_HOLIDAY_NAMES, 'lao': _CN_TO_LO_HOLIDAY_NAMES,
            'tamil': _CN_TO_TA_HOLIDAY_NAMES, 'telugu': _CN_TO_TE_HOLIDAY_NAMES,
        }

        name_map = _holiday_name_maps.get(current_language)
        if name_map:
            holiday_data = {}
            for yr, entries in _cn_holiday_data.items():
                holiday_data[yr] = {name_map.get(cn_name, cn_name): date for cn_name, date in entries.items()}
        else:
            holiday_data = _cn_holiday_data

        if year not in holiday_data:
            return f"Holiday data for year {year} not found"

        assert holiday_name and holiday_name.strip(), "Holiday name cannot be empty"
        year_holidays = holiday_data[year]
        holiday_names = list(year_holidays.keys())
        matched_holidays = process.extract(holiday_name, holiday_names, limit=None, scorer=fuzz.partial_ratio)
        if matched_holidays and matched_holidays[0][1] >= 80:
            matched_holiday = matched_holidays[0][0]
            return year_holidays[matched_holiday]
        else:
            return f"Holiday named '{holiday_name}' not found in year {year}"

    @is_tool(ToolType.READ)
    def get_user_historical_behaviors(self) -> str:
        return str(self.db.user_historical_behaviors)

    @is_tool(ToolType.READ)
    def get_user_all_orders(self) -> str:
        if self.db.orders is None:
            return "User currently has no order information"
        orders_repr = "\n".join([repr(order) for order in self.db.orders.values()])
        return orders_repr

    @is_tool(ToolType.READ)
    def get_nearby(self, longitude: float, latitude: float, range: float) -> str:
        target_list = []

        if hasattr(self.db, "stores"):
            for store in self.db.stores.values():
                distance = self.longitude_latitude_to_distance(longitude, latitude, store.location.longitude,
                                                               store.location.latitude)
                if distance <= range:
                    target_list.append(str(store))

        if hasattr(self.db, "shops"):
            for shop in self.db.shops.values():
                distance = self.longitude_latitude_to_distance(longitude, latitude, shop.location.longitude,
                                                               shop.location.latitude)
                if distance <= range:
                    target_list.append(str(shop))

        if hasattr(self.db, "hotels"):
            for hotel in self.db.hotels.values():
                distance = self.longitude_latitude_to_distance(longitude, latitude, hotel.location.longitude,
                                                               hotel.location.latitude)
                if distance <= range:
                    target_list.append(str(hotel))

        if hasattr(self.db, "attractions"):
            for attraction in self.db.attractions.values():
                distance = self.longitude_latitude_to_distance(longitude, latitude, attraction.location.longitude,
                                                               attraction.location.latitude)
                if distance <= range:
                    target_list.append(str(attraction))

        if hasattr(self.db, "flights"):
            for flight in self.db.flights.values():
                dep_distance = self.longitude_latitude_to_distance(longitude, latitude,
                                                                   flight.departure_airport_location.longitude,
                                                                   flight.departure_airport_location.latitude)
                if dep_distance <= range:
                    target_list.append(str(flight))
                    continue

                arr_distance = self.longitude_latitude_to_distance(longitude, latitude,
                                                                   flight.arrival_airport_location.longitude,
                                                                   flight.arrival_airport_location.latitude)
                if arr_distance <= range:
                    target_list.append(str(flight))

        if hasattr(self.db, "trains"):
            for train in self.db.trains.values():
                dep_distance = self.longitude_latitude_to_distance(longitude, latitude,
                                                                   train.departure_station_location.longitude,
                                                                   train.departure_station_location.latitude)
                if dep_distance <= range:
                    target_list.append(str(train))
                    continue

                arr_distance = self.longitude_latitude_to_distance(longitude, latitude,
                                                                   train.arrival_station_location.longitude,
                                                                   train.arrival_station_location.latitude)
                if arr_distance <= range:
                    target_list.append(str(train))

        if len(target_list) == 0:
            return "No search results found"
        return "\n".join(target_list)

    def get_now(self, format_str):
        if self.db.time is not None and len(self.db.time) > 0:
            return self.db.time
        return get_now(format_str)


class ToolSignature(BaseModel):
    """A signature of a tool."""

    name: Annotated[str, Field(description="The name of the tool")]
    doc: Annotated[str, Field(description="The documentation of the tool")]
    params: Annotated[
        Optional[dict],
        Field(description="JSON schema of the parameters of the tool", default=None),
    ]
    returns: Annotated[
        Optional[dict],
        Field(description="JSON schema of the return of the tool", default=None),
    ]


def get_tool_signatures(tools: ToolKitBase) -> dict[str, ToolSignature]:
    """Get all the tool signatures from a tool kit.

    Returns:
        A dictionary of tool signatures.
    """
    signatures = {}
    for name, tool in tools.get_tools().items():
        signatures[name] = ToolSignature(
            name=name,
            doc=str(tool),
            params=tool._serialize_params(tool.params),
            returns=tool._serialize_returns(tool.returns),
        )
    return signatures


def get_tool_types(tools: ToolKitBase) -> dict[str, ToolType]:
    """Get the type of a tool.

    Returns:
        A dictionary of tool types.
    """
    return {name: tools.tool_type(name) for name in tools.get_tools().keys()}
