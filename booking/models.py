#python built-in library
from datetime import datetime, timedelta
import json
#django built-in library
from django.core.serializers import serialize
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.views import View
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
#third party library
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.authtoken.models import Token
#project library
from member.models import Member
from driver.models import Driver

class RideBooking(models.Model):
    MOTOR = 0
    MOBIL = 1
    VEHICLE_TYPE_CHOICES = (
        (MOTOR, 'Motor'),
        (MOBIL, 'Mobil'),
    )
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    destination_latitude = models.CharField(blank=True, null=True, max_length=55)
    destination_longitude = models.CharField(blank=True, null=True, max_length=55)
    destination_address = models.CharField(max_length=255, blank=True)
    pick_up_address = models.CharField(max_length=255, blank=True)
    pick_up_latitude = models.CharField(blank=True, null=True, max_length=55)
    pick_up_longitude = models.CharField(blank=True, null=True, max_length=55)
    booking_no = models.CharField(blank=True, null=True, max_length=22)
    booking_time = models.DateTimeField(default= datetime.now())
    pick_up_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    vehicle_type = models.PositiveSmallIntegerField(choices=VEHICLE_TYPE_CHOICES, default=MOTOR) #done
    fee = models.IntegerField(default=0)

    def __str__(self):
        return self.destination_address.upper()

    def get_number(amount = 8, is_ride = False):
        if not is_ride:
            prefix = "ABDLVR"
        else:
            prefix = "ABRIDE"
        random_number = get_random_string(amount, 
            allowed_chars='0123456789')
        return "{}-{}".format(prefix, random_number)



class DeliveryBooking(models.Model):
    MOTOR = 0
    MOBIL = 1
    VEHICLE_TYPE_CHOICES = (
        (MOTOR, 'Motor'),
        (MOBIL, 'Mobil'),
    )
    member = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    destination_latitude = models.FloatField(blank=True, null=True, max_length=55)
    destination_longitude = models.FloatField(blank=True, null=True, max_length=55)
    destination_address = models.CharField(max_length=255, blank=True)
    pick_up_address = models.CharField(max_length=255, blank=True)
    pick_up_latitude = models.FloatField(blank=True, null=True, max_length=55)
    pick_up_longitude = models.FloatField(blank=True, null=True, max_length=55)
    booking_no = models.CharField(blank=True, null=True, max_length=22)
    booking_time = models.DateTimeField(default= datetime.now())
    pick_up_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    vehicle_type = models.PositiveSmallIntegerField(choices=VEHICLE_TYPE_CHOICES, default=MOTOR) #done
    recipient_name = models.CharField(max_length=255, default='')
    phone_regex = RegexValidator(regex=r'^0\d{9,15}$', message="Nomor Telepon Harus memiliki format 0819999999'. Maksimal 15 Digit.")
    recipient_phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    total_weight = models.IntegerField(default=0)
    fee = models.IntegerField(default=0)

    def __str__(self):
        return self.destination_address.upper()

    
@receiver(post_save, sender=RideBooking)
def RideCallback(sender, instance, created, *args, **kwargs):
    if created:
        is_duplicate = True
        booking_no = RideBooking.get_number(is_ride=True)

        while is_duplicate:
            try:
                RideBooking.objects.get(booking_no = booking_no)
            except:
                is_duplicate = False
        instance.pick_up_time = instance.booking_time + timedelta(hours=1)
        instance.booking_no = booking_no
        instance.save()
        group_name = 'booking_lobby'
        channel_layer = get_channel_layer()
        token = Token.objects.get(user=instance.member.user).key
        async_to_sync(channel_layer.group_send)(group_name, 
            {'type': 'chat_message', 
            'token': token,
            "message": json.dumps(json.loads(serialize('json', [instance]))[0]['fields']),
            "username": instance.member.user.username})

@receiver(post_save, sender=DeliveryBooking)
def DeliveryCallback(sender, instance, created, *args, **kwargs):
    if created:
        is_duplicate = True
        booking_no = RideBooking.get_number(is_ride=False)
        while is_duplicate:
            try:
                DeliveryBooking.objects.get(booking_no = booking_no)
            except:
                is_duplicate = False
        instance.pick_up_time = instance.booking_time + timedelta(hours=1)
        instance.booking_no = booking_no
        instance.save()
        group_name = 'booking_lobby'
        channel_layer = get_channel_layer()
        token = Token.objects.get(user=instance.member.user).key
        async_to_sync(channel_layer.group_send)(group_name, 
            {'type': 'chat_message', 
            'token': token,
            "message": json.dumps(json.loads(serialize('json', [instance]))[0]['fields']),
            "username": instance.member.user.username})