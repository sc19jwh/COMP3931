# Generated by Django 4.1.4 on 2023-03-30 19:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0018_remove_destination_order_destination_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='destination',
            name='end_date',
        ),
    ]