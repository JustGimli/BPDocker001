# Generated by Django 4.2.2 on 2023-07-30 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='consultation',
            name='end_time',
            field=models.DateTimeField(),
        ),
    ]
