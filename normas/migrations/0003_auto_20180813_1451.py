# Generated by Django 2.0.7 on 2018-08-13 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('normas', '0002_empresa_funcionario'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='gerentePK',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='codigo',
            field=models.IntegerField(default=0, unique=True),
        ),
    ]