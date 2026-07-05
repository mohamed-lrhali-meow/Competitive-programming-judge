n , target = map(int,input().split())
a = list(map(int,input().split()))
for i in range(n) :
            for j in range(n) :
                if a[i]+a[j] == target and not(a[i] is a[j]):
                    print(i,j)
                    exit()