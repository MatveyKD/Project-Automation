# Generated by Django 4.0.5 on 2023-10-29 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0023_alter_student_registration_time_alter_student_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='registration_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]