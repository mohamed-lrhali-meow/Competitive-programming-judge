import random
n = random.randint(1,8)
unique_numbers = [random.randint(-10, 10) for _ in range(n)]

print(*unique_numbers)