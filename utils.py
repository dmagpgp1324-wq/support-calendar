import re
from datetime import datetime


def parse_date(text):
    if not text:
        return None

    text = text.strip()
    text = text.replace(".", "-").replace("/", "-")
    text = re.sub(r"\s+", "", text)

    try:
        return datetime.strptime(text[:10], "%Y-%m-%d").date()
    except:
        return None


def extract_period(text):
    """
    예:
    2026-04-01 ~ 2026-04-15
    2026.04.01 ~ 2026.04.15
    같은 형식에서 시작일/종료일 추출
    """
    if not text:
        return None, None, False

    raw = text.strip()

    # 상시공고 처리
    if "상시" in raw or "수시" in raw or "예산 소진시까지" in raw:
        date_match = re.search(r"(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})", raw)
        start_date = parse_date(date_match.group(1)) if date_match else None
        return start_date, None, True

    # 기간형 추출
    match = re.search(
        r"(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2}).*?[~～\-].*?(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})",
        raw
    )
    if match:
        start_date = parse_date(match.group(1))
        end_date = parse_date(match.group(2))
        return start_date, end_date, False

    # 날짜 하나만 있는 경우
    one = re.search(r"(\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})", raw)
    if one:
        d = parse_date(one.group(1))
        return d, None, False

    return None, None, False
