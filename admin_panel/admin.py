from django.contrib import admin

from .models import Student, StudentTeam, ProjectManager, Team


class StudentTeamQuantityInline(admin.TabularInline):
    model = StudentTeam
    extra = 1
    fields = ['student', ]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'level', ]
    list_display = ['full_name', 'username', 'registration_time', 'period_requested', 'level', 'status', ]
    ordering = ['full_name']


@admin.register(ProjectManager)
class ProjectManagerAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_display = ['full_name', 'telegram_nickname', 'telegram_chat_id', 'period', ]
    ordering = ['full_name']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ['project_manager', 'level', 'status', ]
    list_display = ['timeslot', 'project_manager', 'level', 'status', 'brief', 'trello_board_link']
    list_filter = ['project_manager', 'timeslot', 'status', ]
    ordering = ['project_manager', 'timeslot', ]
    inlines = [StudentTeamQuantityInline, ]
