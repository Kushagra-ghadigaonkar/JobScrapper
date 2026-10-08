import sqlite3
from pathlib import Path

from src.models import Job


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Database directory
DATA_DIR = BASE_DIR / "data"

# SQLite database
DATABASE = DATA_DIR / "jobs.db"


def get_connection():
    # Create data directory if it doesn't exist
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(str(DATABASE))


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            external_id TEXT NOT NULL,
            company TEXT NOT NULL,
            title TEXT NOT NULL,
            location TEXT,
            workplace_type TEXT,
            description TEXT,
            job_url TEXT NOT NULL,
            apply_url TEXT,
            published_at TEXT,
            discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            score INTEGER,
            match_level TEXT,
            status TEXT DEFAULT 'new',
            UNIQUE(source, external_id)
        )
        """
    )

    connection.commit()
    connection.close()


def save_job(job: Job):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO jobs (
            source,
            external_id,
            company,
            title,
            location,
            workplace_type,
            description,
            job_url,
            apply_url,
            published_at,
            score,
            match_level
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            job.source,
            job.external_id,
            job.company,
            job.title,
            job.location,
            job.workplace_type,
            job.description,
            job.job_url,
            job.apply_url,
            job.published_at,
            job.score,
            job.match_level,
        ),
    )

    inserted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return inserted