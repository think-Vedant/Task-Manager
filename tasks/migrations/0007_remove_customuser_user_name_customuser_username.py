# Generated by Django 5.1.7 on 2025-04-02 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_alter_customuser_user_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='user_name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
