import requests

from src.models import Job


BASE_URL = "https://api.lever.co/v0/postings"


def fetch_lever_jobs(
    company: str,
    board: str
) -> list[Job]:

    url = f"{BASE_URL}/{board}"

    params = {
        "mode": "json"
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for item in data:

        categories = item.get(
            "categories",
            {}
        )

        location = categories.get(
            "location",
            ""
        )

        workplace_type = categories.get(
            "commitment",
            ""
        )

        description = (
            item.get("descriptionPlain")
            or item.get("description")
            or ""
        )

        # Try to get the most recent available date
        published_at = (
            item.get("updated_at")
            or item.get("createdAt")
            or item.get("created_at")
        )

        jobs.append(
            Job(
                source="lever",
                external_id=item.get(
                    "id",
                    ""
                ),
                company=company,
                title=item.get(
                    "text",
                    ""
                ),
                location=location,
                workplace_type=workplace_type,
                description=description,
                job_url=item.get(
                    "hostedUrl",
                    ""
                ),
                apply_url=item.get(
                    "applyUrl",
                    ""
                ),
                published_at=published_at
            )
        )

    return jobs