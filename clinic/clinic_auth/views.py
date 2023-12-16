from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializer import UserSerializer
from django.contrib.auth import authenticate
from .models import User
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required


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
def register(request):
    data = {
        'email': request.data.get("email"),
        'password': request.data.get("password"),
    }
    try:
        User.objects.create_user(data['email'], data['password'])
        return Response(f'User created\nemail:{data["email"]}\npassword:{data["password"]}')
    except IntegrityError:
        return Response('This email is already taken')


@api_view(('GET',))
def who(request):
    if not request.user:
        return Response("Authorization error, try login again!")
    return Response(request.user.get_full_name())


@api_view(('PUT',))
def edit(request):
    if not request.user:
        return Response("Authorization error, try login again!")

    data = {
        'email': request.data.get("email"),
        'password': request.data.get("password"),
        'first_name': request.data.get("first_name"),
        'last_name': request.data.get("last_name"),
        'middle_name': request.data.get("middle_name")
    }

    ff = False
    if data['email']:
        request.user.email = data['email']
        ff = True
    if data['password']:
        request.user.password = data['password']
        ff = True
    if data['first_name']:
        request.user.first_name = data['first_name']
        ff = True
    if data['last_name']:
        request.user.last_name = data['last_name']
        ff = True
    if data['middle_name']:
        request.user.middle_name = data['middle_name']
        ff = True
    request.user.save()

    if ff:
        return Response("Updated successfully!")
    return Response("You need to provide at least 1 field!")
