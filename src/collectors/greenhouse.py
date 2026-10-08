import requests

from src.models import Job


BASE_URL = "https://boards-api.greenhouse.io/v1/boards"


def fetch_greenhouse_jobs(company: str, board: str) -> list[Job]:

    url = f"{BASE_URL}/{board}/jobs"

    params = {
        "content": "true"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for item in data.get("jobs", []):

        location = (
            item.get("location", {})
            .get("name", "")
        )

        jobs.append(
            Job(
                source="greenhouse",
                external_id=str(item.get("id")),
                company=company,
                title=item.get("title", ""),
                location=location,
                workplace_type="",
                description=item.get("content", ""),
                job_url=item.get("absolute_url", ""),
                apply_url=item.get("absolute_url", ""),
                published_at=item.get("updated_at")
            )
        )

    return jobs