# Generated by Django 4.1.7 on 2023-05-14 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("RT_app", "0023_infrastructure_masque"),
    ]

    operations = [
        migrations.AlterField(
            model_name="infrastructure",
            name="nom",
            field=models.CharField(max_length=40),
        ),
    ]