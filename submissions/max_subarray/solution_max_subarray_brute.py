a = list(map(int, input().strip().split()))
n = len(a)
m = a[0]
for i in range(n):
    for j in range(i, n):
        s = sum(a[i:j+1])
        m = max(m, s)
print(m)