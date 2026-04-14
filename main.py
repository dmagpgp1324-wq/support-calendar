from datetime import date, timedelta

from crawlers.bizinfo import crawl_bizinfo
from crawlers.kstartup import crawl_kstartup
from crawlers.modoo import crawl_modoo
from calendar_builder import create_ics_files


def fill_test_dates(notices):
    today = date.today()

    for i, n in enumerate(notices):
        if not n.start_date:
            n.start_date = today + timedelta(days=i)
        if not n.end_date:
            n.end_date = n.start_date + timedelta(days=7)

    return notices


def dedupe(notices):
    result = []
    seen = set()

    for n in notices:
        key = n.key()
        if key in seen:
            continue
        seen.add(key)
        result.append(n)

    return result


def main():
    notices = []

    notices += crawl_bizinfo()
    notices += crawl_kstartup()
    notices += crawl_modoo()

    print("원본 수집 개수:", len(notices))

    notices = fill_test_dates(notices)
    notices = dedupe(notices)

    print("중복 제거 후 개수:", len(notices))

    create_ics_files(notices, "output")

    print("완료!")
    print("output/support_ongoing.ics")
    print("output/support_start.ics")
    print("output/support_deadline.ics")


if __name__ == "__main__":
    main()
