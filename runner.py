import subprocess

compile_result = subprocess.run(["g++", "solution.cpp", "-o", "solution"], capture_output=True, text= True)

if compile_result.returncode == 0:
    try:
        run_result = subprocess.run(["./solution"], input="5 10\n",timeout = 2.0, capture_output= True, text= True)
        if run_result.returncode == 0:
            if run_result.stdout.strip() == "15":
                print(run_result.stdout,"\n","ACCEPTED1")
            else:
                print("Wrong Answer")
        else:
            print("RUNTIME ERROR!")

    except subprocess.TimeoutExpired:
        print("TLE!")
else:
    print("Error!")
    print(compile_result.stderr)