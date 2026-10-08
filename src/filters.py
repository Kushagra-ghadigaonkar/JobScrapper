from datetime import datetime, timedelta, timezone


def is_recent_job(published_at, days=7):
    """
    Return True if the job was posted/updated within the last `days` days.
    """

    if not published_at:
        return False

    try:
        # Handle ISO timestamps such as:
        # 2026-10-05T12:30:00Z
        date_string = published_at.replace("Z", "+00:00")

        job_date = datetime.fromisoformat(date_string)

        # If the timestamp has no timezone, treat it as UTC
        if job_date.tzinfo is None:
            job_date = job_date.replace(tzinfo=timezone.utc)

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

        return job_date >= cutoff_date

    except (ValueError, TypeError):
        return False