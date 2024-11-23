from sharedapp.models import SharedModel
from django.db import models

class EmployeeModel(SharedModel):
    first_name = models.CharField(max_length=255, blank=False, null=False, default='', db_index=True)
    last_name = models.CharField(max_length=255, blank=False, null=False, default='', db_index=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    image = models.ImageField(upload_to='employees/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=False, null=False, unique=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        indexes = [
            models.Index(fields=['first_name', 'last_name']),
        ]


class EmployeeAttendanceModel(SharedModel):
    employee = models.ForeignKey(EmployeeModel, on_delete=models.CASCADE, related_name='attendances', db_index=True)
    device_id = models.IntegerField(db_index=True)
    image = models.ImageField(upload_to='employees/attendances/')
    datetime = models.DateTimeField(db_index=True)
    score = models.FloatField(db_index=True)

    def __str__(self):
        return f'{self.datetime} {self.employee}'

    class Meta:
        indexes = [
            models.Index(fields=['datetime', 'employee']),
        ]