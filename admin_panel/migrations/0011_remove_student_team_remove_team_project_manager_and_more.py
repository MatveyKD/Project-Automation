# Generated by Django 4.0.5 on 2023-10-27 16:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0010_student_period_requested'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='team',
        ),
        migrations.RemoveField(
            model_name='team',
            name='project_manager',
        ),
        migrations.RemoveField(
            model_name='team',
            name='students',
        ),
        migrations.DeleteModel(
            name='ProjectManager',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Team',
        ),
    ]
