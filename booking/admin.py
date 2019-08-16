from django.contrib import admin
from .models import RideBooking, DeliveryBooking

class RideBookingAdmin(admin.ModelAdmin):
	model = RideBooking

class DeliveryBookingAdmin(admin.ModelAdmin):
	model = DeliveryBooking

admin.site.register(RideBooking, RideBookingAdmin)
admin.site.register(DeliveryBooking, DeliveryBookingAdmin)
