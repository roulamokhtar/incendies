# Generated by Django 3.0.5 on 2020-05-24 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('incendies', '0019_auto_20200523_0106'),
    ]

    operations = [
        
        migrations.AlterField(
            model_name='wilaya',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
