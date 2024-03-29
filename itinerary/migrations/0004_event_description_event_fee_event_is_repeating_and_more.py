# Generated by Django 5.0.1 on 2024-02-26 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0003_itinerary_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='fee',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='is_repeating',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='registration_required',
            field=models.BooleanField(default=False),
        ),
    ]
