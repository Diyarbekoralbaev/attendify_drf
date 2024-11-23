from rest_framework import serializers
from .models import ClientModel, ClientVisitHistoryModel


class ClientVisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientVisitHistoryModel
        fields = '__all__'

    def create(self, validated_data):
        visit_count = validated_data['client'].visit_count
        validated_data['client'].visit_count = visit_count + 1
        validated_data['client'].save()
        return super().create(validated_data)

class ClientSerializer(serializers.ModelSerializer):
    visit_histories = ClientVisitHistorySerializer(many=True, read_only=True)
    class Meta:
        model = ClientModel
        fields = '__all__'
        read_only_fields = ['visit_count', 'visit_histories']
