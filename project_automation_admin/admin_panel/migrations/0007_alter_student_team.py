# Generated by Django 4.0.5 on 2023-10-27 14:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0006_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='team',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='admin_panel.team'),
        ),
    ]
