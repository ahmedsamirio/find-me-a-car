# Generated by Django 3.0.8 on 2020-08-17 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curator', '0004_auto_20200817_0924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='cc',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='ad',
            name='chasis',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='ad',
            name='color',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='ad',
            name='features',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
