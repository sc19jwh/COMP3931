# Generated by Django 4.1.4 on 2023-03-18 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0010_delete_airport'),
        ('flights', '0002_flight_subflight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flight',
            name='destination',
        ),
        migrations.RemoveField(
            model_name='subflight',
            name='airline',
        ),
        migrations.AddField(
            model_name='flight',
            name='trip',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trips.trip'),
        ),
    ]
