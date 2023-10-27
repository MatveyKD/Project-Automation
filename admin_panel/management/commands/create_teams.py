from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, EmptyResultSet

from admin_panel.models import ProjectManager
from admin_panel.models import Student
from admin_panel.models import Team


def create_teams():

    # Проверку наличия студентов для распределения пока опускаем

    pms = ProjectManager.objects.all()
    for pm in pms:
        period = pm.period
        empty_teams = Team.objects.filter(pm=pm, status="empty")
        for team in empty_teams:
            students = Student.objects.filter(status="waiting", requested_period=period).ordered_by("registered")
            # проверить сортировку по дата-время
            levels = ["junior", "beginner+", "beginner"] # можно сделать модель
            for level in levels:
                group_of_students = students.filter(level=level)
                if group_of_students.count >= 3:
                    team.update(level=level, status="full")
                    for student in list(group_of_students)[0:2]:
                        team.students.add(student)
                        Student.objects.get(student=student).update(status="fixed")
                    break
