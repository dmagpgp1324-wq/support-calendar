from icalendar import Calendar, Event
from datetime import datetime, timedelta
import os


def _make_calendar(name: str):
    cal = Calendar()
    cal.add("prodid", "-//Support Calendar//")
    cal.add("version", "2.0")
    cal.add("X-WR-CALNAME", name)
    return cal


def _add_event(cal, title, start_date, end_date, description):
    event = Event()
    event.add("summary", title)
    event.add("dtstamp", datetime.now())

    # 종일 일정
    event.add("dtstart", start_date)

    # ICS는 종료일이 +1 되어야 정상 표시됨
    if end_date:
        event.add("dtend", end_date + timedelta(days=1))
    else:
        event.add("dtend", start_date + timedelta(days=1))

    event.add("description", description)
    cal.add_component(event)


def create_ics_files(notices, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    ongoing_cal = _make_calendar("지원사업_진행중")
    start_cal = _make_calendar("지원사업_시작일")
    deadline_cal = _make_calendar("지원사업_마감일")

    for n in notices:
        desc = f"{n.source_name}\n{n.url}"

        # 1) 진행중 막대 일정
        if n.start_date and n.end_date:
            _add_event(
                ongoing_cal,
                f"[{n.source_name}] {n.title}",
                n.start_date,
                n.end_date,
                desc
            )

        # 2) 시작일 일정
        if n.start_date:
            _add_event(
                start_cal,
                f"🟢 시작 [{n.source_name}] {n.title}",
                n.start_date,
                None,
                desc
            )

        # 3) 마감일 일정
        if n.end_date:
            _add_event(
                deadline_cal,
                f"🔴 마감 [{n.source_name}] {n.title}",
                n.end_date,
                None,
                desc
            )

    with open(os.path.join(output_dir, "support_ongoing.ics"), "wb") as f:
        f.write(ongoing_cal.to_ical())

    with open(os.path.join(output_dir, "support_start.ics"), "wb") as f:
        f.write(start_cal.to_ical())

    with open(os.path.join(output_dir, "support_deadline.ics"), "wb") as f:
        f.write(deadline_cal.to_ical())
