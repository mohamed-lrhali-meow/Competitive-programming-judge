import subprocess
import os
from pathlib import Path

def read_file(command, inp):
    print("about to run:", command)
    try:
        result = subprocess.run(command, input=inp, capture_output=True, text=True, timeout=3)
        print("finished running")
        return result.stdout.strip(), result.returncode, False
    except subprocess.TimeoutExpired:
        print("caught timeout")
        return ("", 0, True)
    
def check_answer(output ,expected, code,i): 
    if code != 0 : 
        print(f"Erorr on test case {i}")
        return "RE"
    else : 
        if output.strip() == expected.strip() : 
            print(f"test case {i} : ACCEPTED !")
            return "AC"
        else:
            print(f"test case {i} : Wrong answer (expected = {expected} , output = {output})")
            return "WA"


def check_files(path,script):
    problem_dir = Path(path)
    files = sorted(problem_dir.glob("*.in"))
    i = 1 
    if script.suffix == '.c':
        compilation_result = compile_submition(path,script)
        compilation_code , compilation_output ,output_path = compilation_result
        command = [output_path]
        if compilation_code != 0 : 
            print(f"Compilation error : {compilation_output}")
            return
    elif script.suffix == '.py' : 
        command = ['python' , script]
    else : 
        return
    for file in files : 
        with open(file,"r")as inp , open(problem_dir/f"{file.stem}.out") as out :  
            result = read_file(command,inp.read().strip())
            output , code , timed_out = result
            if timed_out : 
                print(f"timeout on test case {i}")
                break
            expected = out.read().strip()
            verdict = check_answer(output,expected,code,i)
        if verdict != "AC" :
            break
        i+=1

def compile_submition(problem_dir,path) : 
    output_path = f"{problem_dir/ path.stem}.exe"
    try:
        os.remove(output_path)
    except OSError : 
        pass
    result = subprocess.run(["gcc",path, "-o" ,output_path],capture_output=True,text=True,timeout=10)
    if result.returncode != 0 :
        return result.returncode,result.stderr,output_path
    else : 
        return result.returncode,result.stderr,output_path
if __name__ == "__main__" : 
    p = Path("C:/Users/mohammed/CP judge/basic_judge/A+B")
    s = Path("C:/Users/mohammed/CP judge/basic_judge/A+B/A+B.c")
    check_files(p,s)