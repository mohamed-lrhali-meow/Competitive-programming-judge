import subprocess

def read_file(command, inp):
    try:
        result = subprocess.run(command, input=inp, capture_output=True, text=True, timeout=3)
        return result.stdout.strip(), result.returncode, result.stderr, False
    except subprocess.TimeoutExpired:
        return ("", 0, "", True)

GENERATOR = ["python", "C:/Users/mohammed/CP judge/stress_tester/max_subarray/generator_max_subarray.py"]
BRUTE = ["python", "C:/Users/mohammed/CP judge/submissions/max_subarray/solution_max_subarray_brute.py"]
FAST = ["python", "C:/Users/mohammed/CP judge/submissions/max_subarray/solution_max_subarray_optimized.py"]

NUM_ROUNDS = 100

for round_num in range(1, NUM_ROUNDS + 1):
    gen_result = subprocess.run(GENERATOR, capture_output=True, text=True, timeout=3)
    inp = gen_result.stdout

    brute_out, brute_code, brute_err, brute_timeout = read_file(BRUTE, inp)
    fast_out, fast_code, fast_err, fast_timeout = read_file(FAST, inp)

    if brute_timeout or fast_timeout:
        print(f"Round {round_num}: TIMEOUT on input: {inp}")
        break
    if brute_code != 0:
        print(f"Round {round_num}: BRUTE CRASHED on input: {inp}\n{brute_err}")
        break
    if fast_code != 0:
        print(f"Round {round_num}: FAST CRASHED on input: {inp}\n{fast_err}")
        break
    if brute_out != fast_out:
        print(f"Round {round_num}: MISMATCH on input: {inp}")
        print(f"  brute: {brute_out}")
        print(f"  fast : {fast_out}")
        break
else:
    print(f"All {NUM_ROUNDS} rounds passed.")