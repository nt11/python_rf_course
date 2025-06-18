import matplotlib
matplotlib.use('TkAgg')  # Must be BEFORE importing pyplot
import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Create data
    plt.ion()

    x = [1, 2, 3, 4, 5]
    y = [1, 4, 9, 16, 25]

    # Create figure and axis
    fig, ax = plt.subplots()

    # Plot data
    ax.plot(x, y)

    # Show the plot
    plt.show()

