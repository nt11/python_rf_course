import numpy as np

if __name__ == "__main__":
    print("results")
    print("-------")
    # Create arrays
    arr1 = np.array([1, 2, 3, 4, 5])
    arr2 = np.array([[1, 2, 3],
                    [4, 5, 6]])

    # Basic operations
    print(arr1 * 2)
    print(arr2.sum())
    print(arr2.mean())

    # Reshape and operations
    matrix = np.arange(9).reshape(3, 3)
    print(matrix)

    # Slicing
    print(matrix[1:, 1:])

    # Boolean indexing
    print(matrix[matrix > 5])

    # Array math
    a = np.array([1, 2, 3])
    b = np.array([4, 5, 6])
    print(a * b)
    print(np.dot(a, b))
    print(np.dot(a,matrix))
    print(np.dot(matrix,a))