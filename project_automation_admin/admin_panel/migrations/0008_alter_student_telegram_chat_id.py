# Generated by Django 4.0.5 on 2023-10-27 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_alter_student_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='telegram_chat_id',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]