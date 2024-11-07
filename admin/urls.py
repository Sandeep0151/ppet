from django.urls import path
from . import views


urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("appointments/", views.appointments, name='appointments'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
]