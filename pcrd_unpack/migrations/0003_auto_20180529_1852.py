# Generated by Django 2.0.3 on 2018-05-29 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pcrd_unpack', '0002_solutions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_id', models.IntegerField()),
                ('rarity', models.IntegerField(default=1)),
                ('unit', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='pcrd_unpack.UnitData')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='solutions',
            name='left_rarity',
        ),
        migrations.RemoveField(
            model_name='solutions',
            name='right_rarity',
        ),
        migrations.AlterField(
            model_name='solutions',
            name='left_team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='left_team', to='pcrd_unpack.Teams'),
        ),
        migrations.AlterField(
            model_name='solutions',
            name='right_team',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='right_team', to='pcrd_unpack.Teams'),
        ),
    ]
