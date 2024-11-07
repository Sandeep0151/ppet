from django.shortcuts import render, get_object_or_404
from myapp.models import Appointment
from datetime import datetime


def dashboard(request):
    today = datetime.today().strftime('%m/%d/%Y')
    appointments = Appointment.objects.filter(date=today)
    print(today)
    return render(request, "admin/dashboard.html", {'appointments': appointments})


def appointments(request):
    appointments = Appointment.objects.all ()
    return render(request, "admin/appointments.html", {'appointments': appointments})


def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    return render(request, 'admin/appointment_detail.html', {'appointment': appointment})
