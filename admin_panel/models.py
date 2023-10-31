from django.db import models


class ProjectManager(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    telegram_nickname = models.CharField(max_length=50, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    period = models.CharField(max_length=20)

    class Meta:
        app_label = 'admin_panel'

    def __str__(self):
        return f'{self.full_name} {self.period}'


class StudentTeam(models.Model):
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='students',
        blank=True,
        null=True
    )
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        related_name='student_team',
        blank=True,
        null=True
    )


class Student(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50, blank=True, null=True)
    telegram_chat_id = models.CharField(max_length=50, blank=True, null=True)
    LEVEL = (
        ("beginner", "beginner"),
        ("beginner+", "beginner+"),
        ("junior", "junior")
    )
    level = models.CharField(max_length=50, choices=LEVEL)
    registration_time = models.DateTimeField(blank=True, null=True)
    period_requested = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=50, default="missing")

    class Meta:
        app_label = 'admin_panel'

    def __str__(self):
        return f'{self.full_name} {self.level}'


class Team(models.Model):
    timeslot = models.CharField(max_length=20)
    project_manager = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        verbose_name='project_manager',
        related_name='timeslots_project_manager'
        )
    LEVEL = (
        ("beginner", "beginner"),
        ("beginner+", "beginner+"),
        ("junior", "junior")
    )
    level = models.CharField(max_length=50, choices=LEVEL)
    status = models.CharField(max_length=20, default='empty')
    brief = models.CharField(max_length=20, blank=True, null=True)
    trello_board_link = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        app_label = 'admin_panel'

    def __str__(self):
        return f'{self.project_manager} {self.timeslot} {self.status}'
