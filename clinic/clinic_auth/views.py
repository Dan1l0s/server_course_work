from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from app.permissions import IsAuthenticated
from .models import User


@api_view(('POST',))
def login(request):
    data = {
        'email': request.data.get("email"),
        'password': request.data.get("password")
    }
    user = authenticate(username=data['email'], password=data['password'])
    if user:
        return Response(user.token)
    else:
        return Response("Incorrect email or password!")


@api_view(('POST',))
def signup(request):
    data = {
        'email': request.data.get("email"),
        'password': request.data.get("password"),
    }
    try:
        User.objects.create_user(data['email'], data['password'])
        return Response(f'User created\nemail:{data["email"]}\npassword:{data["password"]}')
    except IntegrityError:
        return Response('This email is already taken')


@api_view(('PUT', 'GET'))
@permission_classes([IsAuthenticated])
def edit(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    match request.method:
        case "GET":
            return Response(request.user.get_full_name())

        case "PUT":
            data = {
                'email': request.data.get("email"),
                'password': request.data.get("password"),
                'first_name': request.data.get("first_name"),
                'last_name': request.data.get("last_name"),
                'middle_name': request.data.get("middle_name")
            }

            if not data['email'] and not data['password'] and not data['last_name'] and not data['first_name'] and not data['middle_name']:
                return Response("You need to provide at least 1 field!")

            if data['email']:
                request.user.email = data['email']
            if data['password']:
                request.user.password = data['password']
            if data['first_name']:
                request.user.first_name = data['first_name']
            if data['last_name']:
                request.user.last_name = data['last_name']
            if data['middle_name']:
                request.user.middle_name = data['middle_name']

            request.user.save()
            return Response("Updated successfully!")
