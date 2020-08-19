# Generated by Django 3.1 on 2020-08-18 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymeter', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='package_type',
            field=models.CharField(blank=True, choices=[('SMALL', 'SMALL'), ('MEDIUM', 'MEDIUM'), ('LARGE', 'LARGE'), ('NONE', 'NONE')], default='NONE', max_length=8),
        ),
    ]
