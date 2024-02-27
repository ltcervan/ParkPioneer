from django.db import migrations, models
import uuid

def generate_uuids_for_events(apps, schema_editor):
    Event = apps.get_model('itinerary', 'Event')  # Replace 'your_app_name' with the name of your app
    for event in Event.objects.all():
        event.temp_uuid = uuid.uuid4()
        event.save()

class Migration(migrations.Migration):

    dependencies = [
        ('itinerary', '0004_event_description_event_fee_event_is_repeating_and_more'),  # Replace '0004_previous_migration' with the actual name of the previous migration
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='temp_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
        migrations.RunPython(generate_uuids_for_events, reverse_code=migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='event',
            name='id',
        ),
        migrations.RenameField(
            model_name='event',
            old_name='temp_uuid',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True),
        ),
    ]
