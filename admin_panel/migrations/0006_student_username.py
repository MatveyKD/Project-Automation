# Generated by Django 4.0.5 on 2023-10-27 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_alter_student_team_alter_team_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='username',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]
