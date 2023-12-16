from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Doctor, Appointment, Clinic
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta, time
from .serializers import AppointmentSerializer, DoctorSerializer, ClinicSerializer


@api_view(('POST',))
def create_doctor(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    # if not request.user.is_staff:
    #     return Response("Unauthorized access")

    data = {
        'first_name': request.data.get("first_name"),
        'last_name': request.data.get("last_name"),
        'middle_name': request.data.get("middle_name"),
        'clinic_id': request.data.get("clinic_id")
    }
    clinic = Clinic.objects.get(id=data['clinic_id'])
    doctor = Doctor.objects.create(first_name=data['first_name'], last_name=data['last_name'], middle_name=data['middle_name'], clinic=clinic)

    interval = timedelta(minutes=15)
    start_time = time(hour=9, minute=0)
    end_time = time(hour=19, minute=45)

    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=7)

    while current_date < end_date:
        current_time = datetime.combine(current_date, start_time)
        while current_time.time() < end_time:
            appointment = Appointment(
                doctor=doctor,
                date=current_date,
                time=current_time
            )
            appointment.save()
            current_time += interval
        current_date += timedelta(days=1)

    return Response('Doctor was created successfully, id: ' + str(doctor.id))


@api_view(('POST',))
def book(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    appointment = Appointment.objects.get(pk=request.data.get("id"))
    if not appointment.user:
        appointment.user = request.user
        appointment.save()
        return Response(f"Appointment for {appointment.date} at {appointment.time} was booked successfully")
    else:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is already booked! Choose a different appointment!")


@api_view(('POST',))
def cancel(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    appointment = Appointment.objects.get(pk=request.data.get("id"))
    if not appointment.user:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is not booked!")
    elif appointment.user != request.user:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is booked by another user!")
    else:
        appointment.user = None
        appointment.save()
        return Response(f"Appointment for {appointment.date} at {appointment.time} is now available for booking!")


@api_view(('GET',))
def appointment_list(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    doctor_id = request.data.get("doctor")
    doctor = Doctor.objects.get(id=doctor_id)
    if not doctor:
        return Response("Incorrect doctor ID!")
    current_datetime = timezone.now()
    available_appointments = Appointment.objects.filter(
        doctor=doctor,
        date__gte=current_datetime.date(),
        user__isnull=True
    )
    if not available_appointments:
        return Response("There are no available appointments")
    serializer = AppointmentSerializer(available_appointments, many=True)
    return Response(serializer.data)


@api_view(('GET',))
def doctors_list(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    doctors = Doctor.objects.filter(clinic__id=request.data.get("id"))
    serializer = DoctorSerializer(doctors, many=True)
    return Response(serializer.data)


@api_view(('POST', 'GET', 'PUT', 'DELETE'))
def clinic(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    data = {
        'clinic_id': request.data.get("clinic_id"),
        'address': request.data.get("address")
    }

    match request.method:
        case "POST":
            # if not request.user.is_staff:
            #     return Response("Unauthorized access")
            if not data['address']:
                return Response("Address required!")
            try:
                clinic = Clinic.objects.create(address=data['address'])
                return Response('Clinic was created successfully, id: ' + str(clinic.id))
            except:
                return Response("There's already a clinic with provided address")

        case "PUT":
            if not data['address'] or not data['clinic_id']:
                return Response("ID and address required")
            clinic = Clinic.objects.get(id=data['clinic_id'])
            if not clinic:
                return Response("There's no such a clinic with provided ID")
            clinic.address = data['address']
            clinic.save()
            return Response("Clinic was updated successfully")

        case "DELETE":
            if not data['clinic_id']:
                return Response("ID is required")
            clinic = Clinic.objects.get(id=data['clinic_id'])
            if not clinic:
                return Response("There's no such a clinic with provided ID")
            clinic.delete()
            return Response("Clinic was deleted successfully")

        case "GET":
            clinic = Clinic.objects.get(id=data["clinic_id"])
            if not clinic:
                clinics = Clinic.objects.all()
                serializer = ClinicSerializer(clinics, many=True)
                return Response(serializer.data)
            serializer = ClinicSerializer(clinic)
            return Response(serializer.data)


@api_view(('GET',))
def self_appointment_list(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    appointments = Appointment.objects.filter(user=request.user)
    print(appointments)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)
