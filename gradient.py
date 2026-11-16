# Gradient Descent Algorithm. Find the local minimum of f(x) = (x + 3)^2

# Define the function
def f(x):
    return (x + 3) ** 2

# Define the derivative
def df(x):
    return 2 * (x + 3)

# Initialize parameters
x = 2
learning_rate = 0.1
iterations = 100

print("Gradient Descent Algorithm")
print("--------------------------")

# Apply Gradient Descent
for i in range(iterations):

    gradient = df(x)

    # Update x
    x = x - learning_rate * gradient

    print(f"Iteration {i+1}: x = {x:.6f}, y = {f(x):.6f}")

# Display final result
print("\nFinal Result:")
print("Local Minimum Point (x):", round(x, 6))
print("Minimum Value (y):", round(f(x), 6))
