# Generated by Django 2.2 on 2019-04-20 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_person_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchange',
            name='meeting',
        ),
        migrations.AddField(
            model_name='exchange',
            name='kingmeeting',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exchange',
            name='queenmeeting',
            field=models.BooleanField(default=False),
        ),
    ]