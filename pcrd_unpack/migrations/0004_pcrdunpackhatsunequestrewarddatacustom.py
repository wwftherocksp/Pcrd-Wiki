# Generated by Django 2.0.3 on 2018-04-16 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcrd_unpack', '0003_hatsunequestrewarddatacustom'),
    ]

    operations = [
        migrations.CreateModel(
            name='PcrdUnpackHatsunequestrewarddatacustom',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('rate', models.FloatField()),
                ('equipment_id', models.IntegerField(blank=True, null=True)),
                ('item_id', models.IntegerField(blank=True, null=True)),
                ('quest_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'pcrd_unpack_hatsunequestrewarddatacustom',
                'managed': False,
            },
        ),
    ]