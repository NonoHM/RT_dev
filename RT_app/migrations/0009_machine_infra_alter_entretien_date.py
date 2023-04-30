# Generated by Django 4.1.7 on 2023-04-30 16:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("RT_app", "0008_alter_entretien_date_alter_infrastructure_id_machine"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="infra",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="RT_app.infrastructure",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="entretien",
            name="date",
            field=models.DateField(
                default=datetime.datetime(2023, 4, 30, 16, 14, 13, 828713)
            ),
        ),
    ]
