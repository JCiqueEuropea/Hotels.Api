from rest_framework import serializers


class CreateReservationSerializer(serializers.Serializer):
    customer_name = serializers.CharField(max_length=255)
    customer_email = serializers.EmailField(max_length=255)
    customer_phone = serializers.CharField(max_length=20)
    room_id = serializers.UUIDField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
