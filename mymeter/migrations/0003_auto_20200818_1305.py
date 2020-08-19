# Generated by Django 3.1 on 2020-08-18 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mymeter', '0002_accounts_package_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactions',
            old_name='value',
            new_name='grid_value',
        ),
        migrations.AddField(
            model_name='transactions',
            name='vspp_value',
            field=models.FloatField(blank=True, default=0),
            preserve_default=False,
        ),
    ]
