# Generated by Django 5.2 on 2025-04-12 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_usermodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
