# Generated by Django 4.0.5 on 2023-10-27 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0009_alter_student_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='period_requested',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
