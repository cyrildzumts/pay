from rest_framework import serializers
from accounts.models import AvailableService


class AvailableServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableService
        fields = ['service_code', 'name', 'operator', 'category', 'created_at', 'created_by', 'description', 'is_active']