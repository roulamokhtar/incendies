# Generated by Django 3.0.5 on 2020-05-26 01:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0021_auto_20200526_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organisme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.DeleteModel(
            name='Especesincendie',
        ),
    ]
