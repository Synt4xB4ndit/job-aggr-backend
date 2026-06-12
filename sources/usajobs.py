import requests

from config import (
    USAJOBS_EMAIL,
    USAJOBS_API_KEY
)

from models.job import Job


def search_usajobs(keyword: str):

    url = (
        "https://data.usajobs.gov/api/search"
        f"?Keyword={keyword}"
    )

    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": USAJOBS_EMAIL,
        "Authorization-Key": USAJOBS_API_KEY
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    jobs = []

    results = (
        data["SearchResult"]
        ["SearchResultItems"]
    )

    for item in results:

        desc = item[
            "MatchedObjectDescriptor"
        ]

        salary = None

        if desc.get(
            "PositionRemuneration"
        ):
            pay = desc[
                "PositionRemuneration"
            ][0]

            salary = (
                f"${pay['MinimumRange']} - "
                f"${pay['MaximumRange']}"
            )

        jobs.append(
            Job(
                title=desc["PositionTitle"],
                company=desc["OrganizationName"],
                location=desc[
                    "PositionLocation"
                ][0]["LocationName"],
                source="USAJobs",
                apply_url=desc["PositionURI"],
                salary=salary,
                remote=False,
                job_type="Government"
            )
        )

    return jobs