# Generated by Django 3.0.5 on 2020-05-11 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0010_auto_20200512_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incendie',
            name='heureDepart',
            field=models.DateTimeField(blank=True, default='2020-06-01', null=True),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureIntervention',
            field=models.DateTimeField(blank=True, default='2020-06-01', null=True),
        ),
    ]
