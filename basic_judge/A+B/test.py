import subprocess
from pathlib import Path
dir = Path("basic_judge/A+B")
files = sorted(dir.glob("*.in"))
i = 1
for f in files: 
    with open(f"{f}",'r') as inp, open(dir / f"{f.stem}.out",'r') as outp : 
        s1 = inp.read().strip()
        try:
            result = subprocess.run(["python","basic_judge/A+B/A+B.py"],input=s1,capture_output=True,text=True,timeout=2)
            expected = outp.read().strip() 
            if result.returncode != 0 : 
                print("Erorr try again!")
                break
            else : 
                if result.stdout.strip() == expected.strip() : 
                    print(f"test case {i} : ACCEPTED !")
                else:
                    print(f"test case {i} : Wrong answer (expected = {expected} , output = {result.stdout})")
                    break
        except subprocess.TimeoutExpired as e : 
            print(f"test case {i} : Timed out after {e.timeout} seconds !")
            break
    i+=1