# Generated by Django 2.0.7 on 2018-11-27 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('normas', '0002_auto_20181127_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='normapdf',
            name='norma_paiFK',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='normas.NormaPDF'),
        ),
    ]
