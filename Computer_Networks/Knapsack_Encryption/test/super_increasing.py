import random

def generate_superincreasing_knapsack(n):
    knapsack = []
    total = 0
    for i in range(n):
        element = total + 1  # Make sure the next element is greater than the sum of previous elements
        knapsack.append(element)
        total += element
    return knapsack

# Example usage:
n = 20
superincreasing_knapsack = generate_superincreasing_knapsack(n)
print("Super-increasing knapsack of", n, "elements:", superincreasing_knapsack)


# pvt_key = generate_superincreasing_knapsack(6)
# print(pvt_key)