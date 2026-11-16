
n = int(input("Enter number of items: "))

w = list(map(int, input("Enter weights: ").split()))
p = list(map(int, input("Enter profits: ").split()))

capacity = int(input("Enter capacity: "))

items = []

for i in range(n):
    items.append((p[i]/w[i], w[i], p[i]))

items.sort(reverse=True)

total = 0

for ratio, weight, profit in items:
    if capacity >= weight:
        total += profit
        capacity -= weight
    else:
        total += ratio * capacity
        break

print("Maximum Profit:", total)
