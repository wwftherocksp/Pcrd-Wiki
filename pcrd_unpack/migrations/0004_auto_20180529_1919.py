# Generated by Django 2.0.3 on 2018-05-29 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcrd_unpack', '0003_auto_20180529_1852'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teams',
            name='unit',
        ),
        migrations.AddField(
            model_name='teams',
            name='units',
            field=models.ManyToManyField(to='pcrd_unpack.UnitData'),
        ),
    ]
