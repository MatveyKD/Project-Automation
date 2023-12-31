# Generated by Django 4.2.6 on 2023-10-26 21:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_remove_student_requsted_period_student_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='admin_panel.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='students',
            field=models.ManyToManyField(related_name='students', to='admin_panel.student'),
        ),
    ]
