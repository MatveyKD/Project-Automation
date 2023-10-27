# Generated by Django 4.0.5 on 2023-10-27 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0008_alter_student_telegram_chat_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='admin_panel.team'),
        ),
    ]
