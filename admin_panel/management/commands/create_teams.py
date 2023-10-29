from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, EmptyResultSet

from django.core.management.base import BaseCommand
from admin_panel.models import ProjectManager
from admin_panel.models import Student
from admin_panel.models import Team


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_project_teams()


def create_project_teams():
    # Проверку наличия студентов для распределения пока опускаем
    # for st in Student.objects.all():
    #     if st.status == "fixed":
    #         st.status = "waiting"
    #         st.save()
    # for t in Team.objects.all():
    #     t.status = "empty"
    #     t.students.clear()
    #     t.save()
    pms = ProjectManager.objects.all()
    for pm in pms:
        period = pm.period
        empty_teams = Team.objects.filter(project_manager=pm, status="empty")
        print(pm, period)
        print(empty_teams)
        for team in empty_teams:
            students = Student.objects.filter(status="waiting", period_requested=period).order_by("registration_time")
            # проверить сортировку по дата-время
            levels = ["junior", "beginner+", "beginner"]  # можно сделать модель
            for level in levels:
                group_of_students = students.filter(level=level)
                print(students)
                if group_of_students.count() >= 3:
                    team.level = level
                    team.status = "full"
                    team.save()
                    # print(group_of_students)
                    for student in list(group_of_students)[0:3]:
                        team.students.add(student)
                        student.status = "fixed"
                        student.save()
                        print(student)
                    break

    print("____________________________________")
    for team in Team.objects.all():
        print(team.timeslot, team.students.all())
    for std in Student.objects.all():  # filter(status__in=["waiting", "started", "missing"]):
        # teams = Team.objects.filter(students__contains=std)
        if std.status == "fixed":
            print(std.full_name, std.student_team.all()[0].timeslot)
        else:
            print(std.full_name, "waiting")

    # t = Team.objects.all()[0]
    # print(t)
    # t.students.add(Student.objects.all()[0])
    # print(t.students.all())
    # t.save()
    # print(t.students)
    # print(t)
