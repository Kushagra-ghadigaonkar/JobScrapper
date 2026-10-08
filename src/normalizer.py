import re

from src.models import Job


def clean_text(value: str) -> str:

    if not value:
        return ""

    value = re.sub(
        r"<[^>]+>",
        " ",
        value
    )

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value.strip()


def normalize_job(job: Job) -> Job:

    job.title = clean_text(job.title)

    job.location = clean_text(
        job.location
    )

    job.description = clean_text(
        job.description
    )

    job.company = clean_text(
        job.company
    )

    return job