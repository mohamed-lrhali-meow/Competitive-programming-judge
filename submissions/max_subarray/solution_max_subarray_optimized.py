a = list(map(int, input().strip().split()))
n = len(a)
current = 0
best = 0  # <-- the bug: should start at a[0], not 0
for x in a:
    current = max(x, current + x)
    best = max(best, current)
print(best)