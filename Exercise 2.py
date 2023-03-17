def bigger_is_greater(w):
    n = len(w)
    i = n - 1
    while i > 0 and w[i-1] >= w[i]:
        i -= 1
    if i == 0:
        return "no answer"
    x = i - 1  # pivot
    y = n - 1
    while w[y] <= w[x]:
        y -= 1  # successor
    w = list(w)
    w[x], w[y] = w[y], w[x]
    w[x+1:] = reversed(w[x+1:])
    return "".join(w)

# Read number of test cases
t = int(input().strip())

# Process each test case
for i in range(t):
    w = input().strip()
    result = bigger_is_greater(w)
    print(result)