# Code Sandbox Engine

A backend service that compiles and runs untrusted C++ code inside isolated Docker containers, judging submissions against stored test cases — similar in spirit to how online judges like Codeforces or LeetCode work under the hood.

Built as a personal project to learn backend API design, container isolation, and the security considerations involved in running untrusted code.

## How it works

1. A client submits C++ source code and a `problem_id` to `POST /submit`.
2. The server compiles the code inside an isolated Docker container.
3. If compilation succeeds, the compiled binary is run inside a second, locked-down container against a stored test case.
4. The actual output is compared against the expected output, and a verdict is returned.

Expected outputs are stored server-side and are never accepted from the client, so a submission cannot spoof a correct verdict by simply printing the "expected" answer.

## Verdicts

| Verdict | Meaning |
|---|---|
| `AC` | Accepted — output matches expected output |
| `WA` | Wrong Answer — program ran but output didn't match |
| `COMPILATION_ERROR` | Code failed to compile |
| `RUNTIME_ERROR` | Program crashed or exited with a non-zero status |
| `TIME_LIMIT_EXCEEDED` | Program didn't finish within the time limit |

All five verdicts have been manually tested end-to-end through the live API.

## Security

Since this executes arbitrary, untrusted code, each submission runs in its own isolated container with the following restrictions:

- `--network=none` — no network access, submitted code cannot make external requests
- `--memory=256m` — capped memory usage
- `--pids-limit=64` — capped process count, mitigates fork bombs
- `--cap-drop=ALL` — Linux capabilities stripped
- `--read-only` — container filesystem is read-only outside the mounted working directory
- Each submission compiles into its own temporary directory (via `tempfile.mkdtemp`), which is deleted after execution — no shared state between submissions, and no submitted code ever touches the project's own source directory

## Tech stack

- **Python** / **FastAPI** — API layer
- **C++** — language currently supported for submissions
- **Docker** — isolated compilation and execution
- **Pydantic** — request/response validation

## Running it locally

Requirements: Python 3.12+, Docker Desktop running.

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## Example

**Request** — `POST /submit`
```json
{
  "problem_id": "sum_two_numbers",
  "code": "#include <iostream>\nusing namespace std;\nint main() {\n    int a, b;\n    cin >> a >> b;\n    cout << a + b << endl;\n    return 0;\n}"
}
```

**Response**
```json
{
  "verdict": "AC",
  "stdout": "15\n",
  "stderr": ""
}
```

## Adding a test problem

Create a new folder under `testcases/` named after the problem's ID, containing two plain text files:

```
testcases/
└── your_problem_id/
    ├── input.txt
    └── expected_output.txt
```

## Current limitations / what's next

- Single test case per problem (no batch test cases yet)
- C++ only — multi-language support is planned
- Synchronous execution — a submission blocks the request until it finishes; an async job queue (e.g. Celery + Redis) would be needed to handle concurrent load at scale
- Exact string comparison for verdicts — no tolerance for floating-point precision differences

## Project structure

```
main.py          # FastAPI app and /submit route
runner.py        # compile_code(), execute_code(), check_verdict()
testcase.py      # load_testcase()
models.py        # Pydantic request/response schemas
testcases/       # stored problems (input/expected output pairs)
```
