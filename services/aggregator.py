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


def aggregate_jobs(keyword: str):

    jobs = []

    try:
        jobs.extend(
            search_usajobs(keyword)
        )
    except Exception as e:
        print(
            f"USAJobs Error: {e}"
        )

    try:
        jobs.extend(
            search_themuse(keyword)
        )
    except Exception as e:
        print(
            f"TheMuse Error: {e}"
        )

    try:
        jobs.extend(
            search_jooble(keyword)
        )
    except Exception as e:
        print(
            f"Jooble Error: {e}"
        )

    try:
        jobs.extend(
            search_adzuna(keyword)
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