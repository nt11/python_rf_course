print("Results")
print("-------")

# Create a sample list
fruits = ['apple', 'banana', 'cherry', 'date']

# append() - Adds an element to the end of the list
fruits.append('tomato')
print(fruits)

# extend() - Adds all elements of an iterable to the end of the list
more_fruits = ['fig', 'grape']
fruits.extend(more_fruits)
print(fruits)

# insert() - Inserts an element at a specified position
fruits.insert(2, 'blueberry')
print(fruits)

# remove() - Removes the first occurrence of a specified element
fruits.remove('date')
print(fruits)

# pop() - Removes and returns an element at a specified position (or the last element if no index is specified)
popped_fruit = fruits.pop(3)
print(popped_fruit)
print(fruits)

print("cont.--------------------")
print(fruits)

# index() - Returns the index of the first occurrence of a specified element
banana_index = fruits.index('banana')
print(banana_index)

# count() - Returns the number of occurrences of a specified element
fruit_count = fruits.count('apple')
print(fruit_count)

# sort() - Sorts the list in ascending order
fruits.sort()
print(fruits)

# reverse() - Reverses the order of the list
fruits.reverse()
print(fruits)

# clear() - Removes all elements from the list
fruits.clear()
print(fruits)