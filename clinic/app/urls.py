from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

import app.views as views

urlpatterns = [
    path('doctor/book', views.book),
    path('doctor/cancel', views.cancel),
    path('doctor/list', views.appointment_list),
    path('doctor', views.doctor),
    path('clinic', views.clinic),
    path('appointments', views.self_appointment_list)
]
