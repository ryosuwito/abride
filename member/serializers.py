from django.contrib.auth.models import User

from member.models import Member
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            'email','is_active','is_staff', 'first_name', 'last_name', 'username'
        ]

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Member
        fields = [
            'user','client_name','phone_number'
        ]