# Generated by Django 4.1.4 on 2023-02-05 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_country_is_interrail'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='lat',
            field=models.FloatField(default=1),
        ),
        migrations.AddField(
            model_name='city',
            name='lng',
            field=models.FloatField(default=1),
        ),
    ]
