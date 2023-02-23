# Generated by Django 4.1.4 on 2023-02-23 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_alter_destination_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nationality',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='myapp.country'),
        ),
    ]
