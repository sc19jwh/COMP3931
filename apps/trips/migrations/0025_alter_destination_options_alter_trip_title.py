# Generated by Django 4.1.4 on 2023-04-04 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0024_remove_destination_end_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='destination',
            options={'ordering': ['order']},
        ),
        migrations.AlterField(
            model_name='trip',
            name='title',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
    ]
