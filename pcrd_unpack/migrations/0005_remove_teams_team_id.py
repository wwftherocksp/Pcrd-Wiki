# Generated by Django 2.0.3 on 2018-05-29 11:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pcrd_unpack', '0004_auto_20180529_1919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='team_id',
        ),
    ]