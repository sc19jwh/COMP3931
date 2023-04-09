# Generated by Django 4.1.4 on 2023-03-30 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0013_alter_trip_budget_alter_trip_climate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='destination',
            name='start_date',
        ),
        migrations.AddField(
            model_name='destination',
            name='nights',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='destination',
            name='order',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='trip',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
