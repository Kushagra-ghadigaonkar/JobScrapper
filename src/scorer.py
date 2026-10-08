import re

import yaml

from src.models import Job


def load_profile(
    path: str = "config/profile.yaml"
):

    with open(path, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


def contains_phrase(
    text: str,
    phrase: str
) -> bool:

    text = text.lower()
    phrase = phrase.lower()

    return phrase in text


def calculate_score(
    job: Job,
    profile: dict
) -> tuple[int, str]:

    title = job.title.lower()

    description = job.description.lower()

    location = job.location.lower()

    full_text = (
        f"{title} {description} {location}"
    )

    score = 0

    # -------------------------
    # Role matching
    # -------------------------

    primary_roles = profile.get(
        "primary_roles",
        []
    )

    secondary_roles = profile.get(
        "secondary_roles",
        []
    )

    for role in primary_roles:

        if contains_phrase(title, role):

            score += 25
            break

    else:

        for role in secondary_roles:

            if contains_phrase(title, role):

                score += 15
                break

    # -------------------------
    # Skill matching
    # -------------------------

    skills = profile.get(
        "skills",
        []
    )

    matched_skills = 0

    for skill in skills:

        if contains_phrase(
            full_text,
            skill
        ):

            matched_skills += 1

    score += min(
        matched_skills * 5,
        35
    )

    # -------------------------
    # Experience
    # -------------------------

    experience_levels = profile.get(
        "experience_level",
        []
    )

    for level in experience_levels:

        if contains_phrase(
            full_text,
            level
        ):

            score += 15
            break

    # -------------------------
    # Location
    # -------------------------

    preferred_locations = profile.get(
        "locations",
        []
    )

    for preferred in preferred_locations:

        if contains_phrase(
            location,
            preferred
        ):

            score += 5
            break

    # -------------------------
    # Negative keywords
    # -------------------------

    negative_keywords = profile.get(
        "negative_keywords",
        []
    )

    for keyword in negative_keywords:

        if contains_phrase(
            full_text,
            keyword
        ):

            score -= 20

    # -------------------------
    # Clamp
    # -------------------------

    score = max(
        0,
        min(score, 100)
    )

    # -------------------------
    # Match level
    # -------------------------

    if score >= 90:

        level = "🔥 Excellent"

    elif score >= 75:

        level = "🟢 Strong"

    elif score >= 60:

        level = "🟡 Possible"

    elif score >= 40:

        level = "⚪ Low"

    else:

        level = "❌ Poor"

    return score, level