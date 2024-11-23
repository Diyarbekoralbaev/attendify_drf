from django.db import models
from sharedapp.models import SharedModel


class GenderChoices(models.TextChoices):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'

class ClientModel(SharedModel):
    first_seen = models.DateTimeField(db_index=True)
    last_seen = models.DateTimeField(db_index=True)
    visit_count = models.IntegerField(default=1, db_index=True)
    gender = models.CharField(max_length=10, choices=GenderChoices)
    age = models.IntegerField()
    image = models.ImageField(upload_to='clients/')

    def __str__(self):
        return f'{self.first_seen} {self.last_seen} {self.visit_count}'

    class Meta:
        indexes = [
            models.Index(fields=['first_seen', 'last_seen', 'visit_count']),
        ]


class ClientVisitHistoryModel(SharedModel):
    datetime = models.DateTimeField()
    device_id = models.IntegerField()
    client = models.ForeignKey(ClientModel, on_delete=models.CASCADE, related_name='visit_histories')

    def __str__(self):
        return f'{self.datetime} {self.device_id} {self.client}'