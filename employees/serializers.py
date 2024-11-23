from rest_framework import serializers
from .models import EmployeeModel, EmployeeAttendanceModel


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeModel
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)
        return data



class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendanceModel
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        return super().create(validated_data)

