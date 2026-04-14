import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import BIZINFO_LIST_URL, USER_AGENT
from models import SupportNotice
from utils import parse_date, extract_period


def crawl_bizinfo():
    headers = {"User-Agent": USER_AGENT}
    res = requests.get(BIZINFO_LIST_URL, headers=headers, timeout=20)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    notices = []
    rows = soup.select("table tbody tr")

    for row in rows[:20]:
        cols = row.select("td")
        title_tag = row.select_one("a")

        if not title_tag:
            continue

        title = title_tag.get_text(strip=True)
        href = title_tag.get("href", "").strip()
        url = urljoin(BIZINFO_LIST_URL, href)

        # 기업마당 표 구조 기준
        # 실제 구조가 조금 달라질 수 있어서 안전하게 처리
        category = cols[1].get_text(" ", strip=True) if len(cols) > 1 else None
        period_text = cols[3].get_text(" ", strip=True) if len(cols) > 3 else ""
        organization = cols[4].get_text(" ", strip=True) if len(cols) > 4 else None
        notice_date_text = cols[6].get_text(" ", strip=True) if len(cols) > 6 else ""

        notice_date = parse_date(notice_date_text)
        start_date, end_date, is_rolling = extract_period(period_text)

        notice = SupportNotice(
            source="bizinfo",
            source_name="기업마당",
            title=title,
            url=url,
            notice_date=notice_date,
            start_date=start_date or notice_date,
            end_date=end_date,
            organization=organization,
            is_rolling=is_rolling
        )

        notices.append(notice)

    return notices
