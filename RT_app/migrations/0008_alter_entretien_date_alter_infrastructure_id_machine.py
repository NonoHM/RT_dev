# Generated by Django 4.1.7 on 2023-04-30 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RT_app", "0007_alter_entretien_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entretien",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2023, 4, 30, 16, 10, 20, 161189)
            ),
        ),
        migrations.AlterField(
            model_name="infrastructure",
            name="id_machine",
            field=models.ManyToManyField(
                limit_choices_to={"etat": True}, to="RT_app.machine"
            ),
        ),
    ]