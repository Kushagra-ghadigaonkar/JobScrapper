from src.models import Job
from src.scorer import calculate_score


def test_devops_job_scores_high():

    job = Job(
        source="test",
        external_id="1",
        company="Test Company",
        title="Junior DevOps Engineer",
        location="Mumbai",
        workplace_type="Hybrid",
        description="""
        We are looking for a junior DevOps engineer.

        Requirements:

        AWS
        Linux
        Docker
        Kubernetes
        Terraform
        GitHub Actions

        Experience: 0-1 years.
        """,
        job_url="https://example.com/job",
        apply_url="https://example.com/apply"
    )

    profile = {
        "primary_roles": [
            "DevOps Engineer"
        ],
        "secondary_roles": [],
        "skills": [
            "linux",
            "docker",
            "kubernetes",
            "aws",
            "terraform",
            "github actions"
        ],
        "experience_level": [
            "0-1 years",
            "junior"
        ],
        "locations": [
            "Mumbai"
        ],
        "negative_keywords": [
            "senior",
            "5+ years"
        ]
    }

    score, level = calculate_score(
        job,
        profile
    )

    assert score >= 75