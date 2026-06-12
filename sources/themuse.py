import requests

from models.job import Job


SEARCH_EXPANSIONS = {
    "supervisor": [
        "supervisor",
        "manager",
        "lead",
        "team lead",
        "operations"
    ],
    "warehouse": [
        "warehouse",
        "distribution",
        "fulfillment",
        "inventory",
        "logistics"
    ],
    "manager": [
        "manager",
        "lead",
        "director"
    ]
}


def search_themuse(keyword: str):

    url = "https://www.themuse.com/api/public/jobs"

    jobs = []

    keyword_lower = keyword.lower()

    search_terms = SEARCH_EXPANSIONS.get(
        keyword_lower,
        [keyword_lower]
    )

    for page in range(1, 6):

        response = requests.get(
            url,
            params={"page": page},
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            break

        for item in results:

            title = item.get("name", "")
            title_lower = title.lower()

            if not any(
                term in title_lower
                for term in search_terms
            ):
                continue

            company = "Unknown"

            if item.get("company"):
                company = item["company"].get(
                    "name",
                    "Unknown"
                )

            location = "Unknown"

            locations = item.get(
                "locations",
                []
            )

            if locations:
                location = locations[0].get(
                    "name",
                    "Unknown"
                )

            landing_page = item.get(
                "refs",
                {}
            ).get(
                "landing_page",
                ""
            )

            jobs.append(
                Job(
                    title=title,
                    company=company,
                    location=location,
                    source="The Muse",
                    apply_url=landing_page,
                    remote="remote" in location.lower(),
                    job_type="Unknown"
                )
            )

    return jobs