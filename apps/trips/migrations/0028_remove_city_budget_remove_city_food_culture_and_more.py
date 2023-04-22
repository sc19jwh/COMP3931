# Generated by Django 4.1.4 on 2023-04-21 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0027_remove_city_skyscanner_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='city',
            name='food_culture',
        ),
        migrations.RemoveField(
            model_name='city',
            name='nightlife_level',
        ),
        migrations.RemoveField(
            model_name='city',
            name='tourist_attractions',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='food_culture',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='nightlife_level',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='tourist_attractions',
        ),
        migrations.AddField(
            model_name='city',
            name='accom_budget',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='food_budget',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='accom_budget',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='trip',
            name='food_budget',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='climate',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='climate',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='journey_times',
            field=models.DecimalField(blank=True, decimal_places=9, max_digits=10, null=True),
        ),
    ]