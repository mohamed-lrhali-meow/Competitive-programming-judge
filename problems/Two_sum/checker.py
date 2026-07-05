import sys 

def check(input_text,output_text):
    lines = input_text.strip().split('\n')
    n , target = map(int,lines[0].split())
    a = list(map(int,lines[1].split())) 

    parts = output_text.strip().split()
    
    if len(parts) != 2 : 
        return False, "output was not exactly two numbers"
    
    i, j = int(parts[0]), int(parts[1])
    
    if not(-n<=i<=n-1) or not (-n<=j<=n-1): 
        return False , "indices out of range"
    
    if i%n == j%n : 
        return False , "The two indices point to the same element"
    
    if a[i] + a[j] != target : 
        return False , f"a[{i}]+a[{j}] = {a[i]+a[j]}, expected {target}"

    return True , "Valid"


if __name__ == "__main__" : 
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    with open(input_path) as f : 
        input_text = f.read()
    with open(output_path) as f : 
        output_text = f.read() 
    valid , message = check(input_text,output_text)
    print(message)
    sys.exit(0 if valid else 1)