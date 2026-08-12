import subprocess

compile_result = subprocess.run(["g++", "solution.cpp", "-o", "solution"], capture_output=True, text= True)
if compile_result.returncode == 0:
    print("Success!")
    run_result = subprocess.run(["./solution"], input="5 10\n", capture_output= True, text= True)
print(run_result.stdout)