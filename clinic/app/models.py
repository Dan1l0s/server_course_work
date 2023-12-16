from django.db import models

from clinic_auth.models import User


class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.id


class Doctor(models.Model):
    id = models.AutoField(primary_key=True)

    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def get_full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def get_short_name(self):
        return f'{self.last_name} {self.first_name[0]}. {self.middle_name[0]}'


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
