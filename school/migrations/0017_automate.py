# Generated by Django 3.2.6 on 2023-05-07 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0016_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Automate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_username', models.CharField(max_length=100)),
                ('sheet_url', models.CharField(max_length=100)),
            ],
        ),
    ]
