from django.contrib import admin

from .models import Student, ProjectManager, TimeSlot

admin.site.register(Student)
admin.site.register(ProjectManager)
admin.site.register(TimeSlot)
