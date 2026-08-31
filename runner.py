import subprocess
import tempfile
import os   
import shutil

def compile_code(code: str) -> dict:
    work_dir = tempfile.mkdtemp(prefix="sandbox_")
    src_path = os.path.join(work_dir, "solution.cpp")

    with open(src_path, "w") as f:
        f.write(code)

    compile_cmd = [
        "docker", "run", "--rm",
        "-v", f"{work_dir}:/app",
        "-w", "/app",
        "gcc:latest",
        "g++", "solution.cpp", "-o", "solution_linux"
    ]

    compile_result = subprocess.run(
        compile_cmd,
        capture_output = True,
        text = True
    )
    if compile_result.returncode == 0:
        return {"success": True, "work_dir": work_dir}
    else:
        return {"success": False, "error": compile_result.stderr}

def execute_code(work_dir: str, input_data: str) ->dict:
    run_cmd = [
        "docker", "run", "--rm", "-i",
        "--network", "none",
        "--memory=256m",
        "--cap-drop=ALL",
        "--pids-limit=64",
        "--read-only",
        "-v", f"{work_dir}:/app",
        "-w", "/app",
        "gcc:latest",
        "./solution_linux"
    ]
    try:
        run_result = subprocess.run(
            run_cmd,
            input=input_data,
            timeout=2.0,
            capture_output=True,
            text=True
        )
    except subprocess.TimeoutExpired:
        return {"success" : False, "timeout": True, "stdout": "", "stderr": ""}
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)

    if run_result.returncode == 0:
        return {"success" : True, "timeout": False, "stdout": run_result.stdout, "stderr": run_result.stderr}
    else:
        return {"success" : False,"timeout": False, "stdout": run_result.stdout, "stderr": run_result.stderr}

def check_verdict(actual_output: str, expected_output: str) -> str:
    if actual_output.strip() == expected_output.strip():
        return ("AC")
    else:
        return ("WA")

from testcase import load_testcase

if __name__ == "__main__":
    testcase = load_testcase("sum_two_numbers")

    test_code = """
#include <iostream>
using namespace std;
int main() {
    int a, b;
    cin >> a >> b;
    cout << a + b << endl;
    return 0;
}
"""

    compile_result = compile_code(test_code)
    print("Compile result:", compile_result)

    if compile_result["success"]:
        execute_result = execute_code(compile_result["work_dir"], testcase["input_data"])
        print("Execute result:", execute_result)

        verdict = check_verdict(execute_result["stdout"], testcase["expected_output"])
        print("Verdict:", verdict)
    else:   
        print("Compilation failed, skipping execution.")