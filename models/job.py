from pydantic import BaseModel


class Job(BaseModel):
    title: str
    company: str
    location: str

    source: str
    apply_url: str

    salary: str | None = None

    job_type: str | None = None

    remote: bool = False

    description: str | None = None
    