from rest_framework import serializers


class CreateRoomSerializer(serializers.Serializer):
    hotel_id = serializers.UUIDField()
    number = serializers.CharField(max_length=20)
    room_type = serializers.ChoiceField(choices=["SINGLE", "DOUBLE", "SUITE", "DELUXE"])
    price_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    price_currency = serializers.CharField(max_length=3, default="USD")


class UpdateRoomSerializer(serializers.Serializer):
    number = serializers.CharField(max_length=20, required=False)
    room_type = serializers.ChoiceField(choices=["SINGLE", "DOUBLE", "SUITE", "DELUXE"], required=False)
    price_amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=False)
    price_currency = serializers.CharField(max_length=3, required=False)
    is_active = serializers.BooleanField(required=False)
