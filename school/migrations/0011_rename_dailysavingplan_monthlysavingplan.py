# Generated by Django 3.2.6 on 2023-04-29 14:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0010_dailysavingplan'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DailySavingPlan',
            new_name='MonthlySavingPlan',
        ),
    ]
