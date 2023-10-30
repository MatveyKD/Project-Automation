import pandas as pd
import os
import django

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project_automation_admin.settings'
    )
django.setup()


from admin_panel.models import ProjectManager, Student, Team


def format_data(pm=None):
    data_set = {
        "PM": [], "Timeslot": [], "Level": [], "Students": [], "Brief": [], "Trello": []
    }
    if pm:
        teams = Team.objects.filter(project_manager=pm).all()
    else:
        teams = Team.objects.all()
    for team in teams:
        data_set["PM"].append(team.project_manager.full_name)
        data_set["Timeslot"].append(team.timeslot)
        data_set["Level"].append(team.level)
        students = ""
        for student in team.students.all():
            students += student.student.full_name + ", "
        students = students[:len(students)-2]
        data_set["Students"].append(students)
        data_set["Trello"].append(team.trello_board_link)
        data_set["Brief"].append(team.brief)
    return data_set


def format_data_neuds():
    data_set = {
        "Student": [], "TG-nickname": [], "Level": [], "Status": [], "Period requested": []
    }
    for student in Student.objects.filter(status="waiting"):
        data_set["Student"].append(student.full_name)
        if student.username: data_set["TG-nickname"].append(f"@{student.username}")
        else: data_set["TG-nickname"].append(None)
        data_set["Level"].append(student.level)
        data_set["Status"].append("waiting")
        data_set["Period requested"].append(student.period_requested)
        # data_set["Student"].append(student["Student"])
        # data_set["Level"].append(student["Level"])
        # data_set["Status"].append(student["Status"])
        # data_set["Interval-requested"].append(student["Interval-requested"])
    return data_set


def format_data_students():
    data_set = {
        "Student": [], "TG-nickname": [], "Level": [], "Status": [], "Period requested": [], "Team": []
    }
    for student in Student.objects.all():
        data_set["Student"].append(student.full_name)
        if student.username:
            data_set["TG-nickname"].append(f"@{student.username}")
        else:
            data_set["TG-nickname"].append(None)
        data_set["Level"].append(student.level)
        data_set["Status"].append(student.status)
        data_set["Period requested"].append(student.period_requested)
        if student.student_team.all().count() > 0:
            data_set["Team"].append(student.student_team.all()[0].team.timeslot)
        else:
            data_set["Team"].append(None)
    return data_set


def write_schedule(file_name, pm=None):
    # Writing the data into the excel sheet
    writer_obj = pd.ExcelWriter(f'{file_name}.xlsx', engine='xlsxwriter')
    df = pd.DataFrame(format_data(pm=pm))
    df.to_excel(writer_obj, sheet_name='Команды')
    if not pm:
        df_nd = pd.DataFrame(format_data_neuds())
        df_all = pd.DataFrame(format_data_students())

        df_nd.to_excel(writer_obj, sheet_name='Нераспределенные ученики')
        df_all.to_excel(writer_obj, sheet_name='Все ученики')
    writer_obj.close()
    print('Please check out the Write.xlsx file.')


if __name__ == "__main__":
    write_schedule("Schedule")
