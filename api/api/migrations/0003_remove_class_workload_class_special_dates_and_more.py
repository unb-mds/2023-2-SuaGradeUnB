# Generated by Django 4.2.5 on 2023-11-25 22:07

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20231113_2029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='class',
            name='workload',
        ),
        migrations.AddField(
            model_name='class',
            name='special_dates',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='class',
            name='_class',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='class',
            name='classroom',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='class',
            name='days',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=64), size=None),
        ),
        migrations.AlterField(
            model_name='class',
            name='schedule',
            field=models.CharField(max_length=512),
        ),
        migrations.AlterField(
            model_name='class',
            name='teachers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=256), size=None),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='code',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='name',
            field=models.CharField(max_length=128),
        ),
    ]
