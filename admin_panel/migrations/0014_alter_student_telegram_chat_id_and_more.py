# Generated by Django 4.2.6 on 2023-10-28 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0013_alter_student_period_requested'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='telegram_chat_id',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
