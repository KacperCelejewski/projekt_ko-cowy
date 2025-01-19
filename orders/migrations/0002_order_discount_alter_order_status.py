# Generated by Django 5.1.5 on 2025-01-19 20:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="orders.discount",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(max_length=50),
        ),
    ]
