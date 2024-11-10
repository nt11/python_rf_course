print("Results")
print("-------")
# Sample data
students    = ["Alice", "Bob", "Charlie", "David", "Eve", "Don"]
grades      = [85, 92, 78, 95, 88, 99, 77]
attendances = [90, 85, 95, 92, 98]

# Using map() to create a list of student names in uppercase
uppercase_names = list(map(str.upper, students))
print("Uppercase names:", uppercase_names)

uppercase_names = [name.upper() for name in students]

# Using zip() to combine students with their grades
student_grades = list(zip(students, grades))
print("Student grades:", student_grades)

all_students = {}
for i in range(len(students)):
    try:
        all_students[students[i]] = {"grade": grades[i], "attendance": attendances[i]}
    except Exception:
        break

#make a dictionary from the data
all_students ={}
for i,x in enumerate(students):
    try:
        all_students[x] = {"grade": grades[i], "attendance": attendances[i]}
    except Exception:
        break
print(all_students)
