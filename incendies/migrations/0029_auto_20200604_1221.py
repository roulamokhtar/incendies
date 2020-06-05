# Generated by Django 3.0.5 on 2020-06-04 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0028_auto_20200604_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incendie',
            name='dateIntervention',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureDepart',
            field=models.TimeField(default='00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureExt',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureIntervention',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
