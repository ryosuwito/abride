#python built-in library

#django built-in library
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
#third party library

#project library


# Create your models here.
class Driver(models.Model):
	MOTOR = 0
	MOBIL = 1
	VEHICLE_TYPE_CHOICES = (
		(MOTOR, 'Motor'),
		(MOBIL, 'Mobil'),
	)
	vehicle_type = models.PositiveSmallIntegerField(choices=VEHICLE_TYPE_CHOICES, default=MOTOR) #done
	user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	full_name = models.CharField(max_length=255, default='')
	phone_regex = RegexValidator(regex=r'^0\d{9,15}$', message="Nomor Telepon Harus memiliki format 0819999999'. Maksimal 15 Digit.")
	phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validator haruslah berupa list
	def __str__(self):
		return "{}".format(self.full_name.upper())