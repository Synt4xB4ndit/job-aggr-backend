import requests

from config import (
    ADZUNA_APP_ID,
    ADZUNA_APP_KEY
)

from models.job import Job


def search_adzuna(keyword: str):

    if not ADZUNA_APP_ID:
        return []

    if not ADZUNA_APP_KEY:
        return []

    url = (
        f"https://api.adzuna.com/v1/api/jobs"
        f"/us/search/1"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": 25,
        "what": keyword
    }

    response = requests.get(
        url,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    for item in data.get(
        "results",
        []
    ):

        company = "Unknown"

        if item.get("company"):
            company = item["company"].get(
                "display_name",
                "Unknown"
            )

        location = "Unknown"

        if item.get("location"):
            location = item["location"].get(
                "display_name",
                "Unknown"
            )

        salary = None

        salary_min = item.get(
            "salary_min"
        )

        salary_max = item.get(
            "salary_max"
        )

        if salary_min and salary_max:
            salary = (
                f"${salary_min:,.0f}"
                f" - "
                f"${salary_max:,.0f}"
            )

        jobs.append(
            Job(
                title=item.get(
                    "title",
                    "Unknown"
                ),
                company=company,
                location=location,
                source="Adzuna",
                apply_url=item.get(
                    "redirect_url",
                    ""
                ),
                salary=salary,
                job_type="Unknown",
                remote=False
            )
        )

    return jobs