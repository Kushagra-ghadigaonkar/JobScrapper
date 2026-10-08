from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    source: str
    external_id: str
    company: str
    title: str
    location: str
    workplace_type: str
    description: str
    job_url: str
    apply_url: str
    published_at: Optional[str] = None

    score: int = 0
    match_level: str = ""