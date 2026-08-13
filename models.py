from pydantic import BaseModel


class SubmissionRequest(BaseModel):
    problem_id: str
    code: str


class SubmissionResponse(BaseModel):
    verdict: str
    stdout: str = ""
    stderr: str = ""