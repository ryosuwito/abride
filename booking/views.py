#python built-in library

#django built-in library
from django.shortcuts import render
from django.views import View
#third party library
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
#project library
from booking.models import RideBooking, DeliveryBooking
from booking.serializers import RideBookingSerializer, DeliveryBookingSerializer

class RideBookingView(viewsets.ModelViewSet):
    """
    API endpoint that allows Ride Booking to be viewed or edited.
    """
    queryset = RideBooking.objects.all().order_by('-booking_time')
    serializer_class = RideBookingSerializer

class DeliveryBookingView(viewsets.ModelViewSet):
    """
    API endpoint that allows Delivery Booking to be viewed or edited.
    """
    queryset = DeliveryBooking.objects.all().order_by('-booking_time')
    serializer_class = DeliveryBookingSerializer
    def get(request, *args, **kwargs):
    	return Response