from fastapi import APIRouter

from services.aggregator import aggregate_jobs

router = APIRouter()


@router.get("/jobs")
def search_jobs(
    keyword: str,
    location: str = "",
    remote: bool | None = None,
    source: str | None = None,
):

    print(f"Keyword: {keyword}")
    print(f"Location: {location}")

    jobs = aggregate_jobs(
        keyword=keyword,
        location=location
    )

    if remote is not None:
        jobs = [
            job
            for job in jobs
            if job.remote == remote
        ]

    if source:
        jobs = [
            job
            for job in jobs
            if job.source.lower() == source.lower()
        ]

    return {
        "count": len(jobs),
        "jobs": jobs
    }