print("Results")
print("-------")

# Create a sample list
fruits = ['apple', 'banana', 'cherry', 'date']

# append() - Adds an element to the end of the list
fruits.append('tomato')
#print(fruits)

# extend() - Adds all elements of an iterable to the end of the list
more_fruits = ['fig', 'grape']
fruits.extend(more_fruits)
#print(fruits)

# insert() - Inserts an element at a specified position
fruits.insert(2, 'blueberry')
#print(fruits)

# remove() - Removes the first occurrence of a specified element
fruits.remove('date')
#print(fruits)

# pop() - Removes and returns an element at a specified position (or the last element if no index is specified)
popped_fruit = fruits.pop(3)
#print(popped_fruit)
#print(fruits)


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