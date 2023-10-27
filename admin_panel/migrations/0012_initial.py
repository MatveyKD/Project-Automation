# Generated by Django 4.0.5 on 2023-10-27 16:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_panel', '0011_remove_student_team_remove_team_project_manager_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50, unique=True)),
                ('telegram_nickname', models.CharField(max_length=50, unique=True)),
                ('telegram_chat_id', models.CharField(max_length=50, unique=True)),
                ('period', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100, unique=True)),
                ('username', models.CharField(blank=True, max_length=50, unique=True)),
                ('telegram_chat_id', models.CharField(blank=True, max_length=50, unique=True)),
                ('level', models.CharField(max_length=50)),
                ('registration_time', models.DateTimeField(auto_now_add=True)),
                ('period_requested', models.CharField(blank=True, max_length=15)),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeslot', models.CharField(max_length=20)),
                ('level', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('brief', models.CharField(max_length=20)),
                ('trello_board_link', models.CharField(max_length=100)),
                ('project_manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='timeslots_project_manager', to='admin_panel.projectmanager', verbose_name='project_manager')),
                ('students', models.ManyToManyField(related_name='students', to='admin_panel.student')),
            ],
        ),
        migrations.AddField(
            model_name='student',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='admin_panel.team'),
        ),
    ]
