from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import datetime, timedelta, time

from .models import Doctor, Appointment, Clinic
from .serializers import AppointmentSerializer, DoctorSerializer, ClinicSerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticated


class DoctorView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'doctor_id': request.data.get("doctor_id"),
            'first_name': request.data.get("first_name"),
            'last_name': request.data.get("last_name"),
            'middle_name': request.data.get("middle_name"),
            'clinic_id': request.data.get("clinic_id")
        }
        try:
            doctor = Doctor.objects.get(id=data['doctor_id'])
            serializer = DoctorSerializer(doctor)
            return Response(serializer.data)
        except Doctor.DoesNotExist:
            pass

        doctors = Doctor.objects.filter(clinic__id=data['clinic_id'])
        if not doctors:
            doctors = Doctor.objects.all()
            serializer = DoctorSerializer(doctors, many=True)
            return Response(serializer.data)

        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'doctor_id': request.data.get("doctor_id"),
            'first_name': request.data.get("first_name"),
            'last_name': request.data.get("last_name"),
            'middle_name': request.data.get("middle_name"),
            'clinic_id': request.data.get("clinic_id")
        }

        if not data['last_name'] or not data["first_name"] or not data["middle_name"]:
            return Response("Full name required!")
        try:
            clinic = Clinic.objects.get(id=data['clinic_id'])
        except Clinic.DoesNotExist:
            return Response("Incorrect clinic ID!")

        doctor = Doctor.objects.create(first_name=data['first_name'], last_name=data['last_name'], middle_name=data['middle_name'], clinic=clinic)
        return Response('Doctor was created successfully, id: ' + str(doctor.id))

    def put(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'doctor_id': request.data.get("doctor_id"),
            'first_name': request.data.get("first_name"),
            'last_name': request.data.get("last_name"),
            'middle_name': request.data.get("middle_name"),
            'clinic_id': request.data.get("clinic_id")
        }

        if not data['doctor_id']:
            return Response("Doctor ID is required!")
        if not data['last_name'] and not data['first_name'] and not data['middle_name'] and not data['clinic_id']:
            return Response("No data provided to change!")

        try:
            doctor = Doctor.objects.get(id=data['doctor_id'])
        except Doctor.DoesNotExist:
            return Response("Incorrect doctor ID!")

        if data['clinic_id']:
            try:
                clinic = Clinic.objects.get(id=data['clinic_id'])
                doctor.clinic = clinic
            except Clinic.DoesNotExist:
                if not data['last_name'] and not data['first_name'] and not data['middle_name']:
                    return Response("Incorrect clinic ID")

        if data['first_name']:
            doctor.first_name = data['first_name']
        if data['last_name']:
            doctor.last_name = data['last_name']
        if data['middle_name']:
            doctor.middle_name = data['middle_name']
        doctor.save()
        return Response("Doctor was updated successfully")

    def delete(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'doctor_id': request.data.get("doctor_id"),
        }

        if not data['doctor_id']:
            return Response("ID is required")
        try:
            doctor = Doctor.objects.get(id=data['doctor_id'])
            doctor.delete()
            return Response("Doctor was deleted successfully")
        except Doctor.DoesNotExist:
            return Response("There's no such a doctor with provided ID")


class ClinicView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'clinic_id': request.data.get("clinic_id"),
            'address': request.data.get("address")
        }

        try:
            clinic = Clinic.objects.get(id=data["clinic_id"])
            serializer = ClinicSerializer(clinic)
            return Response(serializer.data)
        except Clinic.DoesNotExist:
            clinics = Clinic.objects.all()
            serializer = ClinicSerializer(clinics, many=True)
            return Response(serializer.data)

    def post(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'clinic_id': request.data.get("clinic_id"),
            'address': request.data.get("address")
        }

        if not data['address']:
            return Response("Address required!")
        try:
            clinic = Clinic.objects.create(address=data['address'])
            return Response('Clinic was created successfully, id: ' + str(clinic.id))
        except:
            return Response("There's already a clinic with provided address")

    def put(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'clinic_id': request.data.get("clinic_id"),
            'address': request.data.get("address")
        }

        if not data['address'] or not data['clinic_id']:
            return Response("ID and address required")
        try:
            clinic = Clinic.objects.get(id=data['clinic_id'])
        except Clinic.DoesNotExist:
            return Response("There's no such a clinic with provided ID")
        clinic.address = data['address']
        clinic.save()
        return Response("Clinic was updated successfully")

    def delete(self, request):
        if not request.user:
            return Response("Authorization error, try login again!")

        data = {
            'clinic_id': request.data.get("clinic_id"),
            'address': request.data.get("address")
        }

        if not data['clinic_id']:
            return Response("ID is required")
        try:
            clinic = Clinic.objects.get(id=data['clinic_id'])
        except Clinic.DoesNotExist:
            return Response("There's no such a clinic with provided ID")
        clinic.delete()
        return Response("Clinic was deleted successfully")


@api_view(('POST',))
@permission_classes([IsAuthenticated])
def book(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    try:
        appointment = Appointment.objects.get(pk=request.data.get("id"))
    except Appointment.DoesNotExist:
        return Response("Incorrect appointment ID")

    if not appointment.user:
        appointment.user = request.user
        appointment.save()
        return Response(f"Appointment for {appointment.date} at {appointment.time} was booked successfully")
    else:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is already booked! Choose a different appointment!")


@api_view(('POST',))
@permission_classes([IsAuthenticated])
def cancel(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    try:
        appointment = Appointment.objects.get(pk=request.data.get("id"))
    except Appointment.DoesNotExist:
        return Response("Incorrect appointment ID")

    if not appointment.user:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is not booked!")
    elif appointment.user != request.user:
        return Response(f"Appointment for {appointment.date} at {appointment.time} is booked by another user!")
    else:
        appointment.user = None
        appointment.save()
        return Response(f"Appointment for {appointment.date} at {appointment.time} is now available for booking!")


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def appointment_list(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    doctor_id = request.data.get("doctor_id")
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response("Incorrect doctor ID!")

    delete_passed_appointments(doctor)
    generate_appointments(doctor)

    available_appointments = Appointment.objects.filter(doctor=doctor, user__isnull=True)
    if not available_appointments:
        return Response("There are no available appointments")
    serializer = AppointmentSerializer(available_appointments, many=True)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def self_appointment_list(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    appointments = Appointment.objects.filter(user=request.user)
    print(appointments)
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


############################### HELPERS FUNCTIONS ############################################################################

def delete_passed_appointments(doctor: Doctor):
    current_datetime = datetime.now()
    passed_appointments = Appointment.objects.filter(
        Q(date__lt=current_datetime.date()) |
        (Q(date=current_datetime.date()) & Q(time__lt=current_datetime.time())),
        doctor=doctor,)
    if passed_appointments.exists():
        passed_appointments.delete()


def generate_appointments(doctor: Doctor):
    interval = timedelta(minutes=15)
    start_time = time(hour=9, minute=0)
    end_time = time(hour=19, minute=45)

    current_date = datetime.now().date()
    end_date = current_date + timedelta(days=7)

    while current_date < end_date:
        existing_appointments = Appointment.objects.filter(doctor=doctor, date=current_date)
        if not existing_appointments.exists():
            current_time = datetime.combine(current_date, start_time)
            while current_time.time() < end_time:
                appointment = Appointment(
                    doctor=doctor,
                    date=current_date,
                    time=current_time.time()
                )
                appointment.save()
                current_time += interval
        current_date += timedelta(days=1)
