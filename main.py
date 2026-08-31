from fastapi import FastAPI, HTTPException
from models import SubmissionRequest, SubmissionResponse
from runner import compile_code, execute_code, check_verdict
from testcase import load_testcase

app = FastAPI(title="Code Sandbox Engine API")
@app.get("/")
def health_check():
    return {"status": "running", "message": "API is online"}
@app.post("/submit", response_model=SubmissionResponse)
def submit_code(submission: SubmissionRequest):
    testcase = load_testcase(submission.problem_id)

    compile_result = compile_code(submission.code)
    if compile_result["success"] == False:
        return SubmissionResponse(verdict="COMPILATION_ERROR", stdout="", stderr=compile_result["error"])

    execute_result = execute_code(compile_result["work_dir"], testcase["input_data"])

    if execute_result["timeout"] == True:
        return SubmissionResponse(verdict="TIME_LIMIT_EXCEEDED", stdout="", stderr="")

    if execute_result["success"] == False:
        return SubmissionResponse(verdict="RUNTIME_ERROR", stdout=execute_result["stdout"], stderr=execute_result["stderr"])

    verdict = check_verdict(execute_result["stdout"], testcase["expected_output"])
    return SubmissionResponse(verdict=verdict, stdout=execute_result["stdout"], stderr=execute_result["stderr"])
