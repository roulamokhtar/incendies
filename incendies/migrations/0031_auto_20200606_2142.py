# Generated by Django 3.0.5 on 2020-06-06 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('incendies', '0030_auto_20200604_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degat',
            name='cout',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, verbose_name='coût monétaire'),
        ),
        migrations.AlterField(
            model_name='degat',
            name='nombre',
            field=models.IntegerField(default=0, null=True, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='espece',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='espece'),
        ),
        migrations.AlterField(
            model_name='espece',
            name='typeformation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='incendies.Typeformation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='incendie',
            name='dateDepart',
            field=models.DateField(verbose_name='date départ'),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='dateExt',
            field=models.DateField(blank=True, null=True, verbose_name="date d'extinction"),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='dateIntervention',
            field=models.DateField(blank=True, null=True, verbose_name="date d'intervention"),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureDepart',
            field=models.TimeField(verbose_name='heure départ'),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureExt',
            field=models.TimeField(blank=True, null=True, verbose_name="heure d'intervention"),
        ),
        migrations.AlterField(
            model_name='incendie',
            name='heureIntervention',
            field=models.TimeField(blank=True, null=True, verbose_name="heure d'intervention"),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='moyenshumain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='incendies.Moyenshumain'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='intervention',
            name='nombrehumain',
            field=models.IntegerField(default=0, null=True, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='moyen',
            name='moyensmateriel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='incendies.Moyensmateriel'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='moyen',
            name='nombremateriel',
            field=models.IntegerField(default=0, null=True, verbose_name='nombre'),
        ),
        migrations.AlterField(
            model_name='moyenshumain',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='ressources humains'),
        ),
        migrations.AlterField(
            model_name='moyensmateriel',
            name='moyenshumain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='incendies.Moyenshumain'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organisme',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='organisme intervention'),
        ),
        migrations.AlterField(
            model_name='typedegat',
            name='name',
            field=models.CharField(max_length=100, null=True, verbose_name='type dégat'),
        ),
        migrations.AlterField(
            model_name='typeformation',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='type formation forestière'),
        ),
        migrations.AlterField(
            model_name='typeformationincendie',
            name='sup',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=4, null=True, verbose_name='superficie'),
        ),
    ]
