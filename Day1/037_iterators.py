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

all_students ={}
for student, grade, attendance in zip(students, grades, attendances):
    all_students[student] = {"grade": grade, "attendance": attendance}
print(all_students)

all_students = {}
all_students = {student: {"grade": grade, "attendance": attendance} for student, grade, attendance in zip(students, grades, attendances)}
print(all_students)

def lauda_student(x):
    return x>90

lauda = list(filter(lauda_student, grades))
print(lauda)

lauda = list(filter(lambda x: x>90, grades))
print(lauda)



lauda = [grade for grade in grades if grade > 90]
print(lauda)

grades_sorted = list(sorted(grades))
print(grades_sorted)


# First, let's zip only students and grades
student_grades = zip(students, grades)

# Then sort by grade (second element of each tuple) in descending order
sorted_students = sorted(
    student_grades,
    key=lambda x: x[1],  # Sort based on the grade
)

for student, grade in sorted_students:
    print(f"{student}: {grade}")
