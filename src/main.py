import yaml

from src.filters import is_recent_job

from src.collectors.greenhouse import (
    fetch_greenhouse_jobs
)

from src.collectors.lever import (
    fetch_lever_jobs
)

from src.database import (
    initialize_database,
    save_job
)

from src.normalizer import (
    normalize_job
)

from src.notifier import (
    send_telegram
)

from src.scorer import (
    calculate_score,
    load_profile
)


def load_sources():

    with open(
        "config/sources.yaml",
        "r",
        encoding="utf-8"
    ) as file:

        return yaml.safe_load(file)


def format_notification(job):

    return f"""
🚨 NEW DEVOPS JOB

{job.match_level}
Match Score: {job.score}/100

💼 {job.title}

🏢 {job.company}

📍 {job.location or "Not specified"}

📅 Posted/Updated:
{job.published_at or "Not specified"}

🛠 Relevant skills detected

🔗 Apply:
{job.apply_url}
""".strip()


def main():

    # --------------------------------
    # Initialize database
    # --------------------------------

    initialize_database()

    # --------------------------------
    # Load profile and sources
    # --------------------------------

    profile = load_profile()

    sources = load_sources()

    all_jobs = []

    # --------------------------------
    # Greenhouse
    # --------------------------------

    for source in sources.get(
        "greenhouse",
        []
    ):

        try:

            jobs = fetch_greenhouse_jobs(
                source["company"],
                source["board"]
            )

            all_jobs.extend(jobs)

        except Exception as error:

            print(
                f"Greenhouse error: {error}"
            )

    # --------------------------------
    # Lever
    # --------------------------------

    for source in sources.get(
        "lever",
        []
    ):

        try:

            jobs = fetch_lever_jobs(
                source["company"],
                source["board"]
            )

            all_jobs.extend(jobs)

        except Exception as error:

            print(
                f"Lever error: {error}"
            )

    # --------------------------------
    # Total jobs collected
    # --------------------------------

    total_jobs = len(all_jobs)

    print(
        f"Collected {total_jobs} jobs."
    )

    # --------------------------------
    # Filter jobs from last 7 days
    # --------------------------------

    recent_jobs = []

    skipped_jobs = 0

    for job in all_jobs:

        job = normalize_job(job)

        if not is_recent_job(
            job.published_at,
            days=7
        ):

            skipped_jobs += 1

            continue

        recent_jobs.append(job)

    print(
        f"Jobs from last 7 days: "
        f"{len(recent_jobs)}"
    )

    print(
        f"Older/unknown-date jobs skipped: "
        f"{skipped_jobs}"
    )

    # --------------------------------
    # Score and save recent jobs
    # --------------------------------

    new_jobs = 0

    for job in recent_jobs:

        score, level = calculate_score(
            job,
            profile
        )

        job.score = score

        job.match_level = level

        inserted = save_job(job)

        if inserted:

            new_jobs += 1

            print(
                f"{job.score:3} | "
                f"{job.title} | "
                f"{job.company}"
            )

            # --------------------------------
            # Telegram notification
            # --------------------------------

            if job.score >= 70:

                send_telegram(
                    format_notification(job)
                )

    # --------------------------------
    # Final summary
    # --------------------------------

    print(
        f"Inserted {new_jobs} new jobs."
    )


if __name__ == "__main__":

    main()