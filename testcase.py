import os


def load_testcase(problem_id: str)-> dict:
    input_path = os.path.join("testcases",problem_id, "input.txt")
    expected_path = os.path.join("testcases", problem_id, "expected_output.txt")

    with open(input_path, "r") as f:
        input_data = f.read()
    with open(expected_path, "r") as f:
            expected_output = f.read()   
    return {"input_data": input_data, "expected_output": expected_output}

if __name__ == "__main__":
    result = load_testcase("sum_two_numbers")
    print(result)