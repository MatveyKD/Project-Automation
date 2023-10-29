import os
import json
from datetime import timedelta
import random

import django
from django.utils import timezone

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
            telegram_chat_id=pm.get('Chat_id'),
            period=pm.get('Periods')
            )


def filling_students_db(student_file):
    with open(student_file, 'r', encoding='utf-8') as students_file:
        data_students = json.load(students_file)

    for student in data_students:
        current_datetime = timezone.now()
        start_date = current_datetime
        end_date = current_datetime + timedelta(weeks=2)
        random_datetime = start_date + timedelta(seconds=random.randint(
            0,
            int((end_date - start_date).total_seconds())
            ))

        Student.objects.create(
            full_name=student.get('Student'),
            username=student.get('Nickname'),
            telegram_chat_id=student.get('Chat_id'),
            level=student.get('Level'),
            registration_time=random_datetime,
            period_requested=student.get('Period_requsted'),
            status=student.get('Status')
        )


def main():
    filling_pms_db('dataPms.json')
    filling_students_db('dataStudents.json')


if __name__ == '__main__':
    main()
