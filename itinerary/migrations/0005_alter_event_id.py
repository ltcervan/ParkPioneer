# Generated by Django 5.0.1 on 2024-02-26 07:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0004_event_description_event_fee_event_is_repeating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
