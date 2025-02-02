# Generated by Django 5.1.4 on 2024-12-17 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='resume',
            old_name='uploaded_at',
            new_name='created_at',
        ),
        migrations.AlterField(
            model_name='resume',
            name='is_latest',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
