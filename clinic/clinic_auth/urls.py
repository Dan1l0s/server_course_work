from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login),
    path('signup', views.signup),
    path('user', views.UserEditView.as_view()),
    path('signup/admin', views.signup_admin),
]
