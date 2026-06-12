from models.job import Job


def search_ziprecruiter(keyword: str):

    return [
        Job(
            title=keyword,
            company="ZipRecruiter Example",
            location="Boston, MA",
            source="ZipRecruiter",
            apply_url="https://www.ziprecruiter.com",
            remote=False,
            job_type="Contract"
        )
    ]