# Generated by Django 4.1.7 on 2023-04-30 16:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RT_app", "0011_rename_infra_machine_id_infrastructure_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="entretien",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2023, 4, 30, 16, 34, 17, 163380)
            ),
        ),
    ]