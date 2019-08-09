from django.db import models

class RideBooking(models.Model):
    destination_latitude = models.CharField(blank=True, null=True, max_length=55)
    destination_longitude = models.CharField(blank=True, null=True, max_length=55)
    destination_address = models.CharField(max_length=255, blank=True)
    pick_up_address = models.CharField(max_length=255, blank=True)
    pick_up_latitude = models.CharField(blank=True, null=True, max_length=55)
    pick_up_longitude = models.CharField(blank=True, null=True, max_length=55)
    booking_time = models.DateTimeField(auto_now=True)
    pick_up_time = models.DateTimeField(auto_now=True)
    vehicle_type = models.CharField(max_length=255, default='')
    full_name = models.CharField(max_length=255, default='')
    client_name = models.CharField(max_length=255, default='')
    fee = models.CharField(max_length=255, default='')

    def __str__(self):
        return '%s - %s - %s'%(self.full_name.title(),self.client_name.title(), self.pick_up_time.upper())


class DeliveryBooking(models.Model):
    destination_latitude = models.CharField(blank=True, null=True, max_length=55)
    destination_longitude = models.CharField(blank=True, null=True, max_length=55)
    destination_address = models.CharField(max_length=255, blank=True)
    pick_up_address = models.CharField(max_length=255, blank=True)
    pick_up_latitude = models.CharField(blank=True, null=True, max_length=55)
    pick_up_longitude = models.CharField(blank=True, null=True, max_length=55)
    booking_time = models.DateTimeField(auto_now=True)
    pick_up_time = models.DateTimeField(auto_now=True)
    vehicle_type = models.CharField(max_length=255, default='')
    full_name = models.CharField(max_length=255, default='')
    client_name = models.CharField(max_length=255, default='')
    recipient_name = models.CharField(max_length=255, default='')
    total_weight = models.CharField(max_length=255, default='')
    fee = models.CharField(max_length=255, default='')

    def __str__(self):
        return '%s - %s - %s'%(self.full_name.title(),self.client_name.title(), self.pick_up_time.upper())

        
