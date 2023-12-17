from django.db import models

from clinic_auth.models import User


class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255, unique=True)

    working_hours = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.id}: {self.address}'


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)

    clinic = models.ForeignKey(Clinic, blank=True, null=True, on_delete=models.SET_NULL)

    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    experience = models.IntegerField(null=True)
    about = models.CharField(max_length=255, null=True)
    working_hours = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_short_name(self):
        return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
