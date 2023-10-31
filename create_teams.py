from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, EmptyResultSet

from django.core.management.base import BaseCommand
from admin_panel.models import ProjectManager
from admin_panel.models import Student
from admin_panel.models import Team
from admin_panel.models import StudentTeam


def create_project_teams():
    # Проверку наличия студентов для распределения пока опускаем
    pms = ProjectManager.objects.all()
    for pm in pms:
        period = pm.period
        empty_teams = Team.objects.filter(project_manager=pm, status="empty")
        for team in empty_teams:
            students = Student.objects.filter(status="waiting", period_requested=period).order_by("registration_time")
            levels = ["junior", "beginner+", "beginner"]
            for level in levels:
                group_of_students = students.filter(level=level)
                if group_of_students.count() >= 3:
                    team.level = level
                    team.status = "full"
                    team.save()
                    for student in list(group_of_students)[0:3]:
                        StudentTeam.objects.get_or_create(student=student, team=team)

                        student.status = "fixed"
                        student.save()
                        print(student)
                    break


if __name__ == "__main__":
    create_project_teams()
