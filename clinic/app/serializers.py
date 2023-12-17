from rest_framework import serializers
from .models import Appointment, Doctor, Clinic


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'date', 'doctor', 'time',)


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ('id', 'last_name', 'first_name', "middle_name", 'about', 'working_hours')


class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
