from django.db import models


class ProjectManager(models.Model):
    full_name = models.CharField(max_length=50, unique=True)
    telegram_nickname = models.CharField(max_length=50, unique=True)
    telegram_chat_id = models.CharField(max_length=50, unique=True)
    period = models.CharField(max_length=20)

    class Meta:
        app_label = 'admin_panel'

    def __str__(self):
        return f'{self.full_name} {self.period}'


class Student(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True)
    telegram_chat_id = models.CharField(max_length=50, unique=True, blank=True)
    level = models.CharField(max_length=50)
    registration_time = models.DateTimeField(auto_now_add=True)
    period_requested = models.CharField(max_length=15, blank=True, null=True)
    status = models.CharField(max_length=50)
    team = models.ForeignKey(
        'Team',
        on_delete=models.CASCADE,
        related_name='teams',
        blank=True,
        null=True
    )

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
    level = models.CharField(max_length=20)
    students = models.ManyToManyField('Student', related_name='students')
    status = models.CharField(max_length=20)
    brief = models.CharField(max_length=20)
    trello_board_link = models.CharField(max_length=100)

    class Meta:
        app_label = 'admin_panel'

    def __str__(self):
        return f'{self.project_manager} {self.timeslot} {self.students}'
