# Generated by Django 4.1.4 on 2023-03-07 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_remove_destinationtransport_trip_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='destinationtransport',
            name='transport_legs',
            field=models.ManyToManyField(blank=True, to='trips.transportleg'),
        ),
    ]
