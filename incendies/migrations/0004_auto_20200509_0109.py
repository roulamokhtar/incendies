# Generated by Django 3.0.5 on 2020-05-09 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0003_incendie_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incendie',
            name='supEstime',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='supPlani',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True),
        ),
    ]
