import requests

from config import JOOBLE_API_KEY
from models.job import Job


SEARCH_EXPANSIONS = {
    "supervisor": [
        "supervisor",
        "manager",
        "lead"
    ],
    "warehouse supervisor": [
        "warehouse supervisor",
        "warehouse manager",
        "distribution supervisor",
        "operations supervisor",
        "fulfillment supervisor",
        "inventory supervisor"
    ]
}


def search_jooble(
    keyword: str,
    location: str = ""
):

    if not JOOBLE_API_KEY:
        return []

    url = (
        f"https://jooble.org/api/"
        f"{JOOBLE_API_KEY}"
    )

    payload = {
        "keywords": keyword,
        "page": 1
    }

    if location.strip():
        payload["location"] = location

    response = requests.post(
        url,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    keyword_lower = keyword.lower()

    allowed_terms = SEARCH_EXPANSIONS.get(
        keyword_lower,
        [keyword_lower]
    )

    for item in data.get("jobs", []):

        title = item.get(
            "title",
            ""
        )

        title_lower = title.lower()

        if not any(
            term in title_lower
            for term in allowed_terms
        ):
            continue

        jobs.append(
            Job(
                title=title,
                company=item.get(
                    "company",
                    "Unknown"
                ),
                location=item.get(
                    "location",
                    "Unknown"
                ),
                source="Jooble",
                apply_url=item.get(
                    "link",
                    ""
                ),
                salary=item.get(
                    "salary"
                ),
                job_type="Unknown",
                remote=False
            )
        )

    return jobs