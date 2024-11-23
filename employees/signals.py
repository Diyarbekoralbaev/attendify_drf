from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import EmployeeModel, EmployeeAttendanceModel
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


@receiver(post_save, sender=EmployeeModel)
def employee_update_handler(sender, instance, created, **kwargs):
    if created:
        event = 'employee_create'
    else:
        event = 'employee_update'
    data = {
        'id': instance.id,
        'first_name': instance.first_name,
        'last_name': instance.last_name,
        'email': instance.email,
        'phone_number': instance.phone_number,
        'image': instance.image.url,
    }
    send_group_event(event, data)

@receiver(post_delete, sender=EmployeeModel)
def employee_delete_handler(sender, instance, **kwargs):
    data = {
        'id': instance.id
    }
    send_group_event('employee_delete', data)

@receiver(post_save, sender=EmployeeAttendanceModel)
def employee_attendance_handler(sender, instance, created, **kwargs):
    if created:
        event = 'employee_attendance'
        data = {
            'employee_id': instance.employee.id,
            'device_id': instance.device_id,
            'image': instance.image.url,
            'datetime': instance.datetime,
            'score': instance.score
        }
        send_group_event(event, data)


@receiver(post_delete, sender=EmployeeAttendanceModel)
def employee_attendance_delete_handler(sender, instance, **kwargs):
    data = {
        'employee_id': instance.employee.id,
        'datetime': instance.datetime
    }
    send_group_event('employee_attendance_delete', data)
