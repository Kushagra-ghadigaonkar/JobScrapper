from datetime import datetime, timedelta, timezone


def is_recent_job(published_at, days=7):
    """
    Return True if the job was posted/updated within the last `days` days.

    Supports:
    - ISO 8601 strings
    - Unix timestamps in seconds
    - Unix timestamps in milliseconds
    """

    if published_at is None:
        return False

    try:
        # Handle Unix timestamp
        if isinstance(published_at, (int, float)):
            # Millisecond timestamp
            if published_at > 10_000_000_000:
                job_date = datetime.fromtimestamp(
                    published_at / 1000,
                    tz=timezone.utc
                )
            else:
                # Second timestamp
                job_date = datetime.fromtimestamp(
                    published_at,
                    tz=timezone.utc
                )

        # Handle ISO date string
        elif isinstance(published_at, str):
            date_string = published_at.strip()

            if not date_string:
                return False

            date_string = date_string.replace(
                "Z",
                "+00:00"
            )

            job_date = datetime.fromisoformat(
                date_string
            )

            if job_date.tzinfo is None:
                job_date = job_date.replace(
                    tzinfo=timezone.utc
                )

        else:
            return False

        cutoff_date = (
            datetime.now(timezone.utc)
            - timedelta(days=days)
        )

        return job_date >= cutoff_date

    except (ValueError, TypeError, OverflowError, OSError):
        return False