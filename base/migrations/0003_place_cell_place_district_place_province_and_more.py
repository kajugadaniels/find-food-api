# Generated by Django 5.0 on 2025-01-12 21:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='cell',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Cell'),
        ),
        migrations.AddField(
            model_name='place',
            name='district',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='District'),
        ),
        migrations.AddField(
            model_name='place',
            name='province',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Province'),
        ),
        migrations.AddField(
            model_name='place',
            name='sector',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Sector'),
        ),
        migrations.AddField(
            model_name='place',
            name='village',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Village'),
        ),
        migrations.AlterField(
            model_name='place',
            name='address',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='place',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='place',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid latitude (-90 to 90).', regex='^-?([1-8]?\\d(\\.\\d+)?|90(\\.0+)?)$')], verbose_name='Latitude'),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid longitude (-180 to 180).', regex='^-?((1[0-7]\\d)|(\\d{1,2}))(\\.\\d+)?$')], verbose_name='Longitude'),
        ),
        migrations.AlterField(
            model_name='place',
            name='main_phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Enter a valid phone number (up to 15 digits).', regex='^\\+?1?\\d{9,15}$')], verbose_name='Main Phone Number'),
        ),
    ]
