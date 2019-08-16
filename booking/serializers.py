from booking.models import RideBooking, DeliveryBooking
from member.serializers import MemberSerializer
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault

class RideBookingSerializer(serializers.HyperlinkedModelSerializer):
	member = MemberSerializer(required=False, read_only=True)
	class Meta:
		model = RideBooking
		fields = [
		'member', 'booking_no', 'id',  'vehicle_type', 'driver',
		'booking_time', 'pick_up_time',
		'destination_latitude', 'destination_longitude', 'destination_address',
		'pick_up_latitude', 'pick_up_longitude', 'pick_up_address','fee'
		]
		read_only_fields = ['booking_no', 'id', 'driver',
		'booking_time', 'pick_up_time']
	def create(self, validated_data):
		booking = RideBooking.objects.create(**validated_data)
		booking.member = self.context['request'].user.member
		booking.save()
		return booking

class DeliveryBookingSerializer(serializers.HyperlinkedModelSerializer):
	member = MemberSerializer(required=False, read_only=True)
	class Meta:
		model = DeliveryBooking
		fields = [
		'member', 'booking_no', 'id', 'vehicle_type', 'driver',
		'destination_latitude', 'destination_longitude', 'destination_address',
		'pick_up_latitude', 'pick_up_longitude', 'pick_up_address','fee',
		'booking_time', 'pick_up_time',
		'recipient_name', 'recipient_phone_number', 'total_weight'
		]
		read_only_fields = ['booking_no', 'id', 'vehicle_type', 'driver',
		'booking_time', 'pick_up_time']
	def create(self, validated_data):
		booking = DeliveryBooking.objects.create(**validated_data)
		booking.member = self.context['request'].user.member
		if booking.total_weight > 10:
			booking.vehicle_type = 1
		booking.destination_address = booking.destination_address.replace(", null, null",".")
		booking.pick_up_address = booking.pick_up_address.replace(", null, null",".")
		booking.save()
		return booking
		