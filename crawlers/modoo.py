import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import MODOO_NOTICE_LIST_URL, USER_AGENT
from models import SupportNotice
from utils import parse_date, extract_period


def crawl_modoo():
    headers = {"User-Agent": USER_AGENT}
    res = requests.get(MODOO_NOTICE_LIST_URL, headers=headers, timeout=20)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")
    notices = []

    # notice 관련 링크만 수집
    links = soup.select("a[href*='/notice/']")
    seen = set()

    for link in links:
        href = link.get("href", "").strip()
        if not href or href.endswith("/list"):
            continue

        full_url = urljoin(MODOO_NOTICE_LIST_URL, href)
        if full_url in seen:
            continue
        seen.add(full_url)

        title = link.get_text(" ", strip=True)
        if not title:
            continue

        # 목록에서 주변 텍스트 확인
        parent_text = link.parent.get_text(" ", strip=True)

        start_date, end_date, is_rolling = extract_period(parent_text)
        notice_date = parse_date(parent_text)

        notice = SupportNotice(
            source="modoo",
            source_name="모두의창업",
            title=title,
            url=full_url,
            notice_date=notice_date,
            start_date=start_date or notice_date,
            end_date=end_date,
            is_rolling=is_rolling
        )

        # 상세 페이지에서 한번 더 날짜 확인
        try:
            detail_res = requests.get(full_url, headers=headers, timeout=20)
            detail_res.raise_for_status()
            detail_soup = BeautifulSoup(detail_res.text, "html.parser")
            detail_text = detail_soup.get_text(" ", strip=True)

            d_start, d_end, d_rolling = extract_period(detail_text)
            d_notice = parse_date(detail_text)

            if d_notice and not notice.notice_date:
                notice.notice_date = d_notice

            if d_start:
                notice.start_date = d_start
            elif not notice.start_date and notice.notice_date:
                notice.start_date = notice.notice_date

            if d_end:
                notice.end_date = d_end

            if d_rolling:
                notice.is_rolling = True

        except Exception:
            pass

        notices.append(notice)

        if len(notices) >= 20:
            break

    return notices
