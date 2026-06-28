from sources.usajobs import search_usajobs
from sources.themuse import search_themuse
from sources.jooble import search_jooble
from sources.adzuna import search_adzuna


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
        "inventory supervisor",
        "fulfillment supervisor"
    ]
}

LOCATION_ALIASES = {
    "westport": [
        "westport",
        "fall river",
        "dartmouth",
        "new bedford"
    ],

    "tiverton": [
        "tiverton",
        "fall river",
        "somerset"
    ],

    "fall river": [
        "fall river",
        "westport",
        "somerset",
        "tiverton"
    ],

    "boston": [
        "boston",
        "south boston",
        "cambridge",
        "quincy",
        "brookline"
    ]
}


def filter_relevant_jobs(
    jobs,
    keyword
):

    keyword_lower = keyword.lower()

    allowed_terms = SEARCH_EXPANSIONS.get(
        keyword_lower,
        [keyword_lower]
    )

    filtered_jobs = []

    for job in jobs:

        title_lower = job.title.lower()

        if any(
            term in title_lower
            for term in allowed_terms
        ):
            filtered_jobs.append(job)

    return filtered_jobs


def filter_by_location(
    jobs,
    location
):

    if not location.strip():
        return jobs

    search = (
        location.lower()
        .replace(",", "")
        .replace("massachusetts", "ma")
        .replace("rhode island", "ri")
        .strip()
    )

    search_locations = LOCATION_ALIASES.get(
        search,
        [search]
    )

    filtered = []

    for job in jobs:

        job_location = (
            job.location.lower()
            .replace(",", "")
            .replace("massachusetts", "ma")
            .replace("rhode island", "ri")
        )

        if any(
            city in job_location
            for city in search_locations
        ):
            filtered.append(job)

    return filtered


def aggregate_jobs(
    keyword: str,
    location: str = ""
):

    jobs = []

    try:
        jobs.extend(
            search_usajobs(
                keyword,
                location
            )
        )
    except Exception as e:
        print(
            f"USAJobs Error: {e}"
        )

    try:
        jobs.extend(
            search_themuse(
                keyword,
                location
            )
        )
    except Exception as e:
        print(
            f"TheMuse Error: {e}"
        )

    try:
        jobs.extend(
            search_jooble(
                keyword,
                location
            )
        )
    except Exception as e:
        print(
            f"Jooble Error: {e}"
        )

    try:
        jobs.extend(
            search_adzuna(
                keyword,
                location
            )
        )
    except Exception as e:
        print(
            f"Adzuna Error: {e}"
        )

    jobs = filter_relevant_jobs(
        jobs,
        keyword
    )

    return jobs