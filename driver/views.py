from django.shortcuts import render
from django.views import View
# Create your views here.
def index(request, *args, **kwargs):
	return render(request,"abride/plugin/driver_index.html")