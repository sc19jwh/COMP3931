# Generated by Django 4.1.4 on 2023-02-12 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_alter_trip_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('country', models.ManyToManyField(to='myapp.country')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.trip')),
            ],
        ),
    ]
