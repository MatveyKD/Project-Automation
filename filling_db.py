import os
import json

import django


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project_automation_admin.settings'
    )
django.setup()


from admin_panel.models import ProjectManager, Student


def filling_pms_db(pms_file):
    with open(pms_file, 'r', encoding='utf-8') as pms_file:
        data_pms = json.load(pms_file)

    for pm in data_pms:
        ProjectManager.objects.create(
            full_name=pm.get('ProjectManager'),
            telegram_nickname=pm.get('Nickname'),
            period=pm.get('Periods')
            )


def filling_students_db(student_file):
    with open(student_file, 'r', encoding='utf-8') as students_file:
        data_students = json.load(students_file)

    for student in data_students:
        Student.objects.create(
            full_name=student.get('Student'),
            username=student.get('Nickname'),
            level=student.get('Level')
        )


def main():
    filling_pms_db('dataPms.json')
    filling_students_db('dataStudents.json')


if __name__ == '__main__':
    main()
