# Generated by Django 4.2.6 on 2023-10-28 20:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0015_alter_student_telegram_chat_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='students',
            field=models.ManyToManyField(blank=True, null=True, related_name='students', to='admin_panel.student'),
        ),
    ]
