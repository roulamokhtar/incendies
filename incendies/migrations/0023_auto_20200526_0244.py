# Generated by Django 3.0.5 on 2020-05-26 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0022_auto_20200526_0238'),
    ]

    operations = [
         
        migrations.AddField(
            model_name='intervention',
            name='organisme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='incendies.Organisme'),
            preserve_default=False,
        ),
    ]
