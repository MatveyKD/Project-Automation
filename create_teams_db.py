import os, django


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    'project_automation_admin.settings'
    )
django.setup()


from admin_panel.models import ProjectManager, Team


def create_empty_teams():
    Team.objects.all().delete()

    for pm in ProjectManager.objects.all():
        period = pm.period
        start_in = int(period[:2]) * 60 + int(period[3:5])
        end_in = int(period[8:10]) * 60 + int(period[11:])
        print(int(period[:2]) * 60, int(period[3:5]))
        print(int(period[8:10]) * 60, int(period[11:]))
        while start_in + 30 <= end_in:
            time_slot = ""
            if start_in//60 < 10: time_slot += "0" + str(start_in//60)
            else: time_slot += str(start_in//60)
            time_slot += ":"
            if start_in % 60 < 10: time_slot += "0" + str(start_in % 60)
            else: time_slot += str(start_in % 60)
            time_slot += " - "
            if (start_in+30)//60 < 10: time_slot += "0" + str((start_in+30)//60)
            else: time_slot += str((start_in+30)//60)
            time_slot += ":"
            if (start_in+30) % 60 < 10: time_slot += "0" + str((start_in+30) % 60)
            else: time_slot += str((start_in+30) % 60)
            # time_slot = f"{start_in//60}:{start_in%60} - {(start_in+30)//60}:{(start_in+30)%60}"

            Team.objects.create(
                project_manager=pm,
                timeslot=time_slot
            )
            start_in += 30
