from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import app.views as views

urlpatterns = [
    path('doctor', views.DoctorView.as_view()),
    path('clinic', views.ClinicView.as_view()),
    path('appointments/book', views.book),
    path('appointments/cancel', views.cancel),
    path('appointments', views.appointment_list),
    path('appointments/my', views.self_appointment_list)
]
