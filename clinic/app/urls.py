from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('edit', views.edit),
    path('who', views.who)
]
