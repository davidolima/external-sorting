import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
file_path = 'results/data_p_ways.csv'  # Replace with the path to your CSV file
data = pd.read_csv(file_path, header=None)

# Assign columns to variables
x = data[1]
y = data[0]

# Plot the graph
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linestyle='-', color='b')

# Label the axes
plt.xlabel('X-axis')
plt.ylabel('Y-axis')

# Add a title
plt.title('Graph of Y vs X')

# Show the graph
plt.grid(True)
plt.show()
