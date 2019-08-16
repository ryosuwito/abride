#python built-in library
import json
#django built-in library
from django.shortcuts import render
from django.views import View
from django.utils.safestring import mark_safe
#third party library
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#project library
from booking.models import RideBooking, DeliveryBooking
from booking.serializers import RideBookingSerializer, DeliveryBookingSerializer


def room(request, room_name):
    return render(request, 'abride/channels.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

class RideBookingView(viewsets.ModelViewSet):
	"""
	API endpoint that allows Ride Booking to be viewed or edited.
	"""
	queryset = RideBooking.objects.all().order_by('-booking_time')
	serializer_class = RideBookingSerializer
	permission_classes = (IsAuthenticated,)

class DeliveryBookingView(viewsets.ModelViewSet):
	"""
	API endpoint that allows Delivery Booking to be viewed or edited.
	"""
	queryset = DeliveryBooking.objects.all().order_by('-booking_time')
	serializer_class = DeliveryBookingSerializer
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		"""
		Optionally restricts the returned purchases to a given user,
		by filtering against a `username` query parameter in the URL.
		"""
		queryset = self.queryset
		is_my_book = self.request.query_params.get('my_book', None)
		if is_my_book :
			queryset = queryset.filter(member=self.request.user.member)
		return queryset

def ride_index(request, *args, **kwargs):
	return render(request,"abride/plugin/booking_index.html",
		{"title":"Ride Books",
		"subtitle":"Daftar Semua Booking Perjalanan ABRide"})


def delivery_index(request, *args, **kwargs):
	bookings = DeliveryBooking.objects.all().order_by("-booking_time")
	return render(request,"abride/plugin/booking_index.html",
		{"bookings":bookings,
		"title":"Delivery Books",
		"subtitle":"Daftar Semua Booking Pengantaran ABRide"})