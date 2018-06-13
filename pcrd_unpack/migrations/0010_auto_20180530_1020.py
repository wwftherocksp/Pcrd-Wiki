# Generated by Django 2.0.3 on 2018-05-30 02:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcrd_unpack', '0009_auto_20180530_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_vote', models.IntegerField(default=0)),
                ('down_vote', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SolutionComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=1000)),
                ('solution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pcrd_unpack.Solution')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rarity_1', models.IntegerField(default=1)),
                ('rarity_2', models.IntegerField(default=1)),
                ('rarity_3', models.IntegerField(default=1)),
                ('rarity_4', models.IntegerField(default=1)),
                ('rarity_5', models.IntegerField(default=1)),
                ('unit_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_1', to='pcrd_unpack.UnitData')),
                ('unit_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_2', to='pcrd_unpack.UnitData')),
                ('unit_3', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_3', to='pcrd_unpack.UnitData')),
                ('unit_4', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_4', to='pcrd_unpack.UnitData')),
                ('unit_5', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unit_5', to='pcrd_unpack.UnitData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='solution',
            name='left_team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_team', to='pcrd_unpack.Team'),
        ),
        migrations.AddField(
            model_name='solution',
            name='right_team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right_team', to='pcrd_unpack.Team'),
        ),
    ]
