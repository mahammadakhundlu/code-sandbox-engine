import subprocess

compile_cmd = [
    "docker", "run", "--rm",
    "-v", f"{subprocess.os.getcwd()}:/app",
    "-w", "/app",
    "gcc:latest",
    "g++", "solution.cpp", "-o", "solution_linux"
]

compile_result = subprocess.run(compile_cmd,
                                capture_output=True,
                                text=True)

if compile_result.returncode == 0:
    try:
        run_cmd = [
            "docker", "run", "--rm", "-i",
            "--network", "none",
            "--memory=256m",
            "-v", f"{subprocess.os.getcwd()}:/app",
            "-w", "/app",
            "gcc:latest",
            "./solution_linux"
        ]

        run_result = subprocess.run(
            run_cmd,
            input="5 10\n",
            timeout=2.0,
            capture_output=True,
            text=True
        )

        if run_result.returncode == 0:
            output = run_result.stdout.strip()
            if output == "15":
                print("ACCEPTED (AC)!")
            else:
                print(f"WRONG ANSWER (WA)! Output: {output}")
        else:
            print("RUNTIME ERROR!")

    except subprocess.TimeoutExpired:
        print("TLE!")
else:
    print("Error!")
    print(compile_result.stderr)