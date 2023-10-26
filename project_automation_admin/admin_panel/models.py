from django.db import models


class ProjectManager(models.Model):
    project_manager = models.CharField(max_length=50, unique=True)
    telegram_nickname = models.CharField(max_length=50, unique=True)
    telegram_chat_id = models.CharField(max_length=50, unique=True)
    period = models.CharField(max_length=20)
    timeslot = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.project_manager}'


class Student(models.Model):
    student = models.CharField(max_length=100, unique=True)
    telegram_nickname = models.CharField(max_length=50, unique=True)
    telegram_chat_id = models.CharField(max_length=50, unique=True)
    level = models.CharField(max_length=50)
    registration_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    requsted_period = models.ForeignKey(
        'TimeSlot',
        on_delete=models.CASCADE,
        verbose_name='period',
        related_name='students_requested_period'
        )
    time_slot = models.ForeignKey(
        'TimeSlot',
        on_delete=models.CASCADE,
        verbose_name='timeslot',
        related_name='students_time_slot'
        )

    def __str__(self):
        return f'{self.full_name} {self.level}'


class TimeSlot(models.Model):
    project_manager = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        verbose_name='project_manager',
        related_name='timeslots_project_manager'
        )
    period = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        verbose_name='period',
        related_name='period_project_manager'
        )
    timeslot = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        verbose_name='timeslot',
        related_name='timeslot_project_manager'
        )
    level = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name='level',
        related_name='student_project_manager'
        )
    students = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    brief = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.project_manager} {self.timeslot} {self.students}'
