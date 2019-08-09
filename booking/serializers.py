from booking.models import RideBooking, DeliveryBooking
from rest_framework import serializers

class RideBookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RideBooking
        fields = [
        'destination_latitude', 'destination_longitude', 'destination_address',
        'pick_up_latitude', 'pick_up_longitude', 'pick_up_address',
        'booking_time', 'pick_up_time', 'full_name', 'client_name', 'fee'
        ]

class DeliveryBookingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DeliveryBooking
        fields = [
        'destination_latitude', 'destination_longitude', 'destination_address',
        'pick_up_latitude', 'pick_up_longitude', 'pick_up_address',
        'booking_time', 'pick_up_time', 'full_name', 'client_name', 'fee',
        'recipient_name', 'total_weight'
        ]
