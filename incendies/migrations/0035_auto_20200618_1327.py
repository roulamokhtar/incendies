# Generated by Django 3.0.5 on 2020-06-18 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0034_auto_20200618_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='limite_commune',
            name='autre_nom',
            field=models.CharField(max_length=30, null=True),
        ),
    ]