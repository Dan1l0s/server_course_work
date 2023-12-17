from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'last_name', 'first_name', 'middle_name', 'birthday', 'insurance_policy_number', 'is_staff')
