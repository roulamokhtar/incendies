# Generated by Django 3.0.5 on 2020-05-27 23:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0024_auto_20200527_1556'),
    ]

    operations = [
        migrations.CreateModel(
            name='Moyenshumain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Typedegat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='Moyensmobilise',
            new_name='Moyensmateriel',
        ),
        migrations.RenameField(
            model_name='intervention',
            old_name='moyensMobilise',
            new_name='moyensmateriel',
        ),
        migrations.RenameField(
            model_name='intervention',
            old_name='nombre',
            new_name='nombrehumain',
        ),
        migrations.AddField(
            model_name='intervention',
            name='nombremateriel',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.CreateModel(
            name='degat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.IntegerField(default=0, null=True)),
                ('cout', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('incendie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incendies.Incendie')),
                ('typedegat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='incendies.Typedegat')),
            ],
        ),
        migrations.AddField(
            model_name='intervention',
            name='moyenshumain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='incendies.Moyenshumain'),
        ),
    ]