# Generated by Django 3.0.5 on 2020-05-10 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0007_auto_20200510_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incendie',
            name='circonscription',
        ),
        migrations.RemoveField(
            model_name='incendie',
            name='wilaya',
        ),
    ]