
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from employees.models import EmployeeAttendanceModel
from .models import ClientModel, ClientVisitHistoryModel
from datetime import datetime
import json

def send_group_event(event_name, data):
    # Serialize datetime objects to strings
    def serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError("Type %s not serializable" % type(obj))

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'broadcast',
        {
            'type': 'send_event',
            'event': event_name,
            'data': json.loads(json.dumps(data, default=serialize)),  # Serialize data
        }
    )

@receiver(post_save, sender=ClientModel)
def client_update_handler(sender, instance, created, **kwargs):
    if created:
        event = 'client_create'
    else:
        event = 'client_update'
    data = {
        'id': instance.id,
        'first_seen': instance.first_seen,
        'last_seen': instance.last_seen,
        'visit_count': instance.visit_count,
        'gender': instance.gender,
        'age': instance.age,
        'image': instance.image.url,
        'visit_histories': [
            {
                'datetime': visit.datetime,
                'device_id': visit.device_id
            }
            for visit in ClientVisitHistoryModel.objects.filter(client=instance).order_by('datetime')
        ]
    }
    send_group_event(event, data)

@receiver(post_delete, sender=ClientModel)
def client_delete_handler(sender, instance, **kwargs):
    data = {
        'id': instance.id
    }
    send_group_event('client_delete', data)


@receiver(post_save, sender=ClientVisitHistoryModel)
def client_visit_history_handler(sender, instance, created, **kwargs):
    if created:
        event = 'client_visit_create'
    else:
        event = 'client_visit_update'
    data = {
        'datetime': instance.datetime,
        'device_id': instance.device_id,
        'client': instance.client.id
    }
    send_group_event(event, data)


@receiver(post_delete, sender=ClientVisitHistoryModel)
def client_visit_history_delete_handler(sender, instance, **kwargs):
    data = {
        'datetime': instance.datetime,
        'device_id': instance.device_id,
        'client': instance.client.id
    }
    send_group_event('client_visit_delete', data)