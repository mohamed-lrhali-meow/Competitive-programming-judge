# Mini Online Judge

A small online judge built from scratch — the kind of system that grades submissions on
platforms like Codeforces or Kattis. Runs Python and C submissions against test cases and
reports a verdict (Accepted, Wrong Answer, Time Limit Exceeded, Runtime Error, Compilation
Error).

Built as a learning project to understand what actually happens after you hit "submit" —
not just to solve more problems, but to build the thing that grades them.

## Why

I've spent a few months doing competitive programming on Codeforces and LeetCode, and got
curious about the mechanics behind a verdict: how does a judge safely run untrusted code,
catch infinite loops, and decide pass/fail without trusting anything about what it's running?
This project is my answer to that question, built incrementally and mostly by hand rather
than generated — the goal is to actually understand every piece, not just have it work.

## Current status

Supports Python and C submissions, multiple test cases per problem, and the following
verdicts:

| Verdict | Meaning |
|---|---|
| `AC` | Accepted — output matches expected exactly (after whitespace normalization) |
| `WA` | Wrong Answer — ran fine, output didn't match |
| `RE` | Runtime Error — submission exited with a nonzero status |
| `TLE` | Time Limit Exceeded — submission didn't finish within the time limit |
| `CE` | Compilation Error — C submission failed to compile (Python submissions skip this step) |

The judge stops at the first failing test case, same as real judges.

## How it works

```
problems/
  A+B/
    1.in   1.out
    2.in   2.out
    ...
    A+B.py   (or A+B.c)
```

A "problem" is a folder containing paired `.in`/`.out` test files. The judge:

1. Looks at the submission's file extension.
   - `.py` → runs it directly with the Python interpreter.
   - `.c` → compiles it with `gcc` first. The old binary (if any) is deleted before
     compiling, so a failed compile can never leave a stale, previously-working binary
     around to be silently re-run.
2. For each test case (discovered automatically via the file system, not hardcoded), runs
   the submission with the `.in` file piped to stdin, and captures stdout, the exit code,
   and whether it timed out.
3. Compares the captured output against the matching `.out` file to decide the verdict.
4. Stops and reports as soon as a test case fails.

### Design notes

- **Runtime errors are detected via exit code, not exceptions.** When a subprocess crashes,
  Python doesn't raise an exception for it — the subprocess just exits normally with a
  nonzero return code, and the crash details end up in its own stderr. The judge checks
  `returncode != 0` explicitly rather than relying on `try/except` to catch a child
  process's failure.
- **Python and C submissions share the same test-running logic.** The only thing that
  differs between them is what *command* gets run — `["python", "sol.py"]` vs
  `["sol.exe"]`. Everything downstream of "run this command against this input" is
  identical, which meant adding C support didn't require rewriting the test-comparison or
  test-discovery logic at all.
- **Compilation happens once per submission, not once per test case**, since the source
  doesn't change between tests — the compiled binary is reused across the whole run.

## Usage

```bash
python judge.py <problem_folder> <submission_file>
```

Example:
```bash
python judge.py problems/A+B problems/A+B/A+B.c
```

## Roadmap

- [x] Core judge loop: run a submission, compare output, report AC/WA/TLE/RE
- [x] Multiple test cases per problem, discovered automatically, stop-at-first-failure
- [x] C submission support: compile step, CE detection, stale-binary protection
- [ ] Refactor: verdicts as return values instead of inline prints, for reuse outside a
      terminal (web UI, logging, etc.)
- [ ] Real resource limits (CPU time + memory) via a small C runner using `setrlimit` /
      `getrusage`, instead of relying on wall-clock timeouts alone
- [ ] Stress-testing tool: random test generation + brute-force vs. optimized diffing
- [ ] Special judges for problems with multiple valid answers
- [ ] Submission history (SQLite)
- [ ] Minimal web UI (Flask)
- [ ] A small set of real seeded problems

## What I learned building this so far

- A crashed subprocess doesn't raise an exception in the parent process — you have to check
  its exit code explicitly.
- String comparison for judging output needs normalization (trailing whitespace/newlines),
  or correct solutions get marked wrong for the wrong reasons.
- `subprocess.run()` with a list of arguments needs each argument as its own separate list
  element — combining them into one string silently does the wrong thing rather than
  raising an error.
- Compiler failures (`gcc`) follow the exact same success/failure convention as any other
  subprocess: exit code `0` for success, nonzero otherwise — a compiler is just another
  program from the caller's point of view.

## About this project

Built independently, step by step, with a deliberate choice to write the implementation by
hand rather than lean on AI to generate it — the point of the project is to actually
understand the mechanics, not just have a working judge.
