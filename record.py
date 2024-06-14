from datetime import datetime
from dataclasses import dataclass
@dataclass
class Record:
        date: datetime
        wdir: float | None
        wspeed: float | None
