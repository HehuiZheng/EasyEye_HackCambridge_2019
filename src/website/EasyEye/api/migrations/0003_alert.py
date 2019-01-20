# Generated by Django 2.1.3 on 2019-01-19 23:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_seconddata_start_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('alert_level', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
    ]
