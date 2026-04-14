from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class SupportNotice:
    source: str
    source_name: str
    title: str
    url: str

    notice_date: Optional[date] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

    organization: Optional[str] = None

    is_rolling: bool = False
    is_closed: bool = False

    def key(self):
        return f"{self.source}_{self.title}_{self.start_date}_{self.end_date}"
