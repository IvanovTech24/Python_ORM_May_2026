import os
import django



# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
# Run and print your queries

from main_app.models import Student

# from main_app.models import Employee
# from django.db import connection, reset_queries
# from pprint import pp
#
#
# all_employee = Employee.objects.all()
# print(all_employee.count())
# first = Employee.objects.first()
# print(first)
# last = Employee.objects.last()
# print(last)
# employee = Employee.objects.get(id=1)
# print(employee)
# create_employee = Employee.objects.create(
#     first_name="John",
#     last_name="Doe", age=30,
#     city="New York", salary=50000,
#     gender="Male",
#     department="Engineering"
# )
# print(create_employee)
# find_female = Employee.objects.filter(gender="Female")
#
# for f in find_female:
#     print(f)
#
# pp(connection.queries)

"""
FC5204	John	Doe	15/05/1995	john.doe@university.com
FE0054	Jane	Smith	null	jane.smith@university.com
FH2014	Alice	Johnson	10/02/1998	alice.johnson@university.com
FH2015	Bob	Wilson	25/11/1996	bob.wilson@university.com

"""

def add_students():
    Student.objects.create(
        student_id='FC5204',
        first_name='John',
        last_name='Doe',
        birth_date='1995-05-15',
        email='john.doe@university.com'
    )


    student_2 = Student(
        student_id='FE0054',
        first_name='Jane',
        last_name='Smith',
        email='jane.smith@university.com'
    )
    student_2.save()


    student_3 = Student()
    student_3.student_id = 'FH2014'
    student_3.first_name = 'Alice'
    student_3.last_name = 'Johnson'
    student_3.birth_date = '1998-02-10'
    student_3.email = 'alice.johnson@university.com'
    student_3.save()


    Student.objects.create(
        student_id='FH2015',
        first_name='Bob',
        last_name='Wilson',
        birth_date='1996-11-25',
        email='bob.wilson@university.com'
    )


def get_students_info():
    all_students = Student.objects.all()
    return '\n'.join(f'Student №{s.student_id}: {s.first_name} {s.last_name}; Email: {s.email}' for s in all_students)

print(get_students_info())


def update_students_emails():
    all_students = Student.objects.all()

    for s in all_students:
        email_parts = s.email.split('@')
        s.email = s.email.replace(email_parts[1], 'uni-students.com')

    Student.objects.bulk_update(all_students, ['email'])

def truncate_students():
    Student.objects.all().delete()