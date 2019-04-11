# Generated by Django 2.2 on 2019-04-11 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_wish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wish',
            name='angel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wishes_to_fulfill', to='books.Person'),
        ),
    ]
