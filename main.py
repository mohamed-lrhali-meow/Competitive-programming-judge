import subprocess
import os
from pathlib import Path

def read_file(command, inp):
    try:
        result = subprocess.run(command, input=inp, capture_output=True, text=True, timeout=3)
        return result.stdout.strip(), result.returncode,result.stderr, False
    except subprocess.TimeoutExpired:
        print("caught timeout")
        return ("", 0,"", True)
    
def check_answer(output ,expected, code,i): 
    if code != 0 : 
        return "RE"
    else : 
        if output.strip() == expected.strip() : 
            return "AC"
        else:
            return "WA"


def check_files(submissions_path,problem_name,test_cases,solution_submitted):
    test_cases_dir = Path(test_cases)
    files = sorted(test_cases_dir.glob("*.in"))
    i = 0
    if solution_submitted.suffix == '.c':
        compilation_result = compile_submition(submissions_path,problem_name)
        compilation_code , compilation_output ,output_path = compilation_result
        command = [output_path]
        if compilation_code != 0 : 
            return "CE",i,compilation_output
    elif solution_submitted.suffix == '.py' : 
        command = ['python' , solution_submitted]
    else : 
        return ("WL",i,"")
    last_result = ()
    for file in files : 
        with open(file,"r")as inp , open(test_cases_dir/f"{file.stem}.out") as out :  
            i+=1
            result = read_file(command,inp.read().strip())
            output , code ,system_out, timed_out = result
            if timed_out : 
                last_result = ("TLE",i,system_out)
                break
            expected = out.read().strip()
            verdict = check_answer(output,expected,code,i)
            last_result = (verdict,i,system_out)
        if verdict != "AC" :
            break
    return last_result

def compile_submition(submissions_path,problem_name) : 
    output_path = f"{submissions_path/problem_name}.exe"
    try:
        os.remove(output_path)
    except OSError : 
        pass
    result = subprocess.run(["gcc",f"{submissions_path/problem_name}.c", "-o" ,output_path],capture_output=True,text=True,timeout=10)
    if result.returncode != 0 :
        return result.returncode,result.stderr,output_path
    else : 
        return result.returncode,result.stderr,output_path
if __name__ == "__main__" : 
    p = Path("C:/Users/mohammed/CP judge/basic_judge/A+B")
    s = Path("C:/Users/mohammed/CP judge/basic_judge/A+B/A+B.c")
    verdict , test_case , system_out  = check_files(p,s) # type: ignore
    if verdict == "AC" : 
        for i in range(1,test_case+1) : 
            print(f"Test case {i} : accepted !")
    elif verdict == "CE" : 
        print("Compilation error!")
    elif verdict == "TLE": 
        print(f"Time limit exceded at test case {test_case}")
    elif verdict == "WL" : 
        print("This judge does not support this language yet!")
    elif verdict == "RE" :
        print(f"Runtime error at test case {test_case}")
    elif verdict == "WA" : 
        print(f"Wrong answer at test case {test_case}")