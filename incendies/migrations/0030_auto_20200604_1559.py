# Generated by Django 3.0.5 on 2020-06-04 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0029_auto_20200604_1221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incendie',
            name='dateExt',
            field=models.DateField(blank=True, null=True),
        ),
    ]
