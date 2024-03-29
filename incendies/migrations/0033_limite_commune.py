# Generated by Django 3.0.5 on 2020-06-17 23:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0032_auto_20200618_0027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Limite_commune',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gid', models.IntegerField()),
                ('objectid_1', models.IntegerField()),
                ('objectid', models.IntegerField()),
                ('objectid_2', models.IntegerField()),
                ('nature', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=30)),
                ('autre_nom', models.CharField(max_length=30)),
                ('nom_wilaya', models.CharField(max_length=30)),
                ('wilaya', models.FloatField()),
                ('origine', models.CharField(max_length=30)),
                ('code', models.IntegerField()),
                ('shape_leng', models.FloatField()),
                ('shape_le_1', models.FloatField()),
                ('shape_le_2', models.FloatField()),
                ('shape_area', models.FloatField()),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
    ]
