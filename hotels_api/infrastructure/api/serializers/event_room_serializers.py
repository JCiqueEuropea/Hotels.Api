from rest_framework import serializers


class CreateEventRoomSerializer(serializers.Serializer):
    hotel_id = serializers.UUIDField()
    name = serializers.CharField(max_length=255)
    capacity = serializers.IntegerField(min_value=1)
    hourly_rate_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    hourly_rate_currency = serializers.CharField(max_length=3, default="USD")


class UpdateEventRoomScheduleSerializer(serializers.Serializer):
    schedule = serializers.JSONField()
