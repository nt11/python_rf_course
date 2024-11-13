import matplotlib.pyplot as plt
import numpy as np

# Create data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)
random_data = np.random.normal(0, 1, 1000)  # For histogram

# Create figure with subplots (3 plots)
plt.figure(figsize=(12, 8))

# Plot 1: Lines
plt.subplot(2, 2, 1)
plt.plot(x, y1, 'b-', label='sin')
plt.plot(x, y2, 'r--', label='cos')
plt.title('Line Plot')
plt.legend()

# Plot 2: Scatter
plt.subplot(2, 2, 2)
plt.scatter(x, y1, c='blue', alpha=0.5, label='sin')
plt.scatter(x, y2, c='red', alpha=0.5, label='cos')
plt.title('Scatter Plot')
plt.legend()

# Plot 3: Histogram
plt.subplot(2, 2, 3)
plt.hist(random_data, bins=30, color='green', alpha=0.7)
plt.title('Histogram')

plt.tight_layout()  # Adjust spacing
plt.show()