from rest_framework import serializers
from .models import ClientModel, ClientVisitHistoryModel


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientModel
        fields = '__all__'
        read_only_fields = ['visit_count', 'visit_history']

    def validate(self, data):
        data = super().validate(data)
        return data


class ClientVisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientVisitHistoryModel
        fields = '__all__'

    def validate(self, data):
        data = super().validate(data)
        return data

    def create(self, validated_data):
        visit_count = validated_data['client'].visit_count
        validated_data['client'].visit_count = visit_count + 1
        validated_data['client'].save()
        return super().create(validated_data)