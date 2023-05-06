# Generated by Django 3.2.6 on 2023-05-06 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0015_rename_dailysavings_dailysaving'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_username', models.CharField(max_length=100)),
                ('message', models.CharField(max_length=300)),
                ('curr_date', models.DateField(auto_now_add=True)),
                ('type_of_letter', models.CharField(max_length=50)),
            ],
        ),
    ]
