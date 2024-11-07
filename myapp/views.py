from django.conf import settings
from django.shortcuts import render, redirect
from reportlab.lib.utils import ImageReader
import io
from reportlab.lib.pagesizes import letter
import base64
from django.core.files.base import ContentFile
import tempfile
import os
from .models import *
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.core.mail import EmailMessage
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
from bs4 import BeautifulSoup
from django.http import HttpResponseServerError
from reportlab.pdfgen import canvas
from django.templatetags.static import static


def generate_otp():
    return str(random.randint(1000, 9999))


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def blog(request):
    return render(request, "blog.html")


def price(request):
    return render(request, "price.html")


def service(request):
    return render(request, "service.html")


def team(request):
    return render(request, "team.html")


def testimonial(request):
    return render(request, "testimonial.html")


def booking(request):
    return render(request, "appointment_booking/booking.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        contactus = ContactUs(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        contactus.save()
        messages.success(request, "Thanks For Contacting Us.")
        return redirect("contact")
    return render(request, "contact.html")


def summary(request):
    try:
        # Render the agreement template to a string
        agreement_content = render_to_string('agreement_template.html')

        # Extract text from the agreement content
        agreement_text = extract_text_from_html(agreement_content)

    except Exception as e:
        print(e)
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        number = request.POST.get("number")
        pet = request.POST.get("pet")
        pet_name = request.POST.get("pet_name")
        pickup_location = request.POST.get("pickup_location")
        drop_location = request.POST.get("drop_location")
        date = request.POST.get("date")
        time = request.POST.get("time")
        selected_service = request.POST.get("selected_service")
        instructions = request.POST.get("instructions")

        request.session["name"] = name
        request.session["email"] = email
        request.session["number"] = number
        request.session["pet"] = pet
        request.session["pet_name"] = pet_name
        request.session["pickup_location"] = pickup_location
        request.session["drop_location"] = drop_location
        request.session["date"] = date
        request.session["time"] = time
        request.session["selected_service"] = selected_service
        request.session["instructions"] = instructions

        context = {
            "name": name,
            "email": email,
            "number": number,
            "pet": pet,
            "pet_name": pet_name,
            "pickup_location": pickup_location,
            "drop_location": drop_location,
            "date": date,
            "time": time,
            "selected_service": selected_service,
            "instructions": instructions,
            "agreement_text": agreement_text
        }
        return render(request, "appointment_booking/appointment_summary.html", context)


def save_appointment(request):
    name = request.session.get("name")
    email = request.session.get("email")
    number = request.session.get("number")
    pet = request.session.get("pet")
    pet_name = request.session.get("pet_name")
    pickup_location = request.session.get("pickup_location")
    drop_location = request.session.get("drop_location")
    date = request.session.get("date")
    time = request.session.get("time")
    selected_service = request.session.get("selected_service")
    instructions = request.session.get("instructions")

    signature_data = request.POST.get("signature")
    signature_name = request.POST.get("signature_name")

    request.session['signature_data'] = signature_data
    request.session["signature_name"] = signature_name

    format, imgstr = signature_data.split(';base64,')  # Get the image format and data
    ext = format.split('/')[-1]  # Extract the image extension (e.g., 'png', 'jpg')
    signature_data_decoded = ContentFile(base64.b64decode(imgstr), name='signature.{}'.format(ext))

    en = Appointment(
        name=name,
        email=email,
        number=number,
        pet=pet,
        pet_name=pet_name,
        pickup_location=pickup_location,
        drop_location=drop_location,
        date=date,
        time=time,
        selected_service=selected_service,
        instructions=instructions,
        signature=signature_data_decoded,
        signature_name=signature_name,
    )
    en.save()
    request.session.clear()

    appointment_template = get_template("appointment_booking/appointment_template.html")
    appointment_context = {
        'appointment': en,
    }
    appointment_html_content = appointment_template.render(appointment_context)
    agreement_template = get_template("email_agreement.html")
    signature_data_decoded = ContentFile(base64.b64decode(imgstr), name='signature.{}'.format(ext))
    signature_data_url = f"data:image/{ext};base64,{imgstr}"
    agreement_context = {
        'appointment': en,
        'signature_image': signature_data_url,
        'signature_name': signature_name,
    }
    agreement_html_content = agreement_template.render(agreement_context)

    combined_html_content = agreement_html_content

    pdf_file = tempfile.NamedTemporaryFile(delete=False)
    pisa_status = pisa.CreatePDF(combined_html_content, dest=pdf_file)
    if not pisa_status.err:
        pdf_file.seek(0)

        subject = 'Your Appointment Details'
        email = EmailMessage(subject, appointment_html_content, to=[email])
        email.content_subtype = "html"
        email.attach('agreement.pdf', pdf_file.read(), 'application/pdf')
        email.send()

        # Send HTML email to your client
        client_subject = '{} has booked an appointment'.format(name)
        client_email = EmailMessage(client_subject, appointment_html_content, to=['p.petarrivals@gmail.com'])
        client_email.content_subtype = "html"
        client_email.send()
        pdf_file.close()
        os.remove(pdf_file.name)  # Clean up the temporary file

        return redirect("success", booking_id=en.booking_id)
    return HttpResponse('PDF generation error occurred.')


def agreement(request):
    signature_data = request.session.get("signature_data")
    signature_name = request.session.get("signature_name")
    return render(request, "email_agreement.html", {"signature_data": signature_data, "signature_name": signature_name})


def success(request, booking_id):
    appointment = Appointment.objects.get(booking_id=booking_id)
    return render(request, "appointment_booking/success.html", {"appointment": appointment})


def download_pdf(request, booking_id):
    # Retrieve appointment details from the database
    appointment = Appointment.objects.get(booking_id=booking_id)

    # Get the HTML template as a string
    template = get_template("appointment_booking/appointment_template.html")
    context = {
        'appointment': appointment,
    }
    html_content = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="appointment_{booking_id}.pdf"'

    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html_content, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response


def print(request):
    return render(request, "appointment_booking/appointment_template.html")


def cancel_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            appointment = Appointment.objects.get(booking_id=booking_id)
            appointment_email = appointment.email

            # Delete the appointment
            appointment.delete()

            # Send cancellation email
            template = get_template("booking_cancellation/cancel_email.html")
            context = {
                "appointment": appointment,
            }
            html_content = template.render(context)
            subject = 'Your Appointment Has Been Canceled'
            email = EmailMessage(subject, html_content, to=[appointment_email])
            email.content_subtype = "html"
            email.send()

            client_subject = 'Appointment Canceled'
            client_email = EmailMessage(client_subject, html_content, to=['p.petarrivals@gmail.com'])
            client_email.content_subtype = "html"
            client_email.send()

            return render(request, "booking_cancellation/cancellation_success.html", {'booking_id': booking_id})
        except Appointment.DoesNotExist:
            return render(request, "booking_cancellation/cancel_booking.html")
    return render(request, "booking_cancellation/cancel_booking.html")


#def view_appointment(request):
#    if request.method == "POST":
#        booking_id = request.POST.get("booking_id")
#        try:
#            appointment = Appointment.objects.get(booking_id=booking_id)
#            return render(request, 'booking_cancellation/view_appointment.html', {'appointment': appointment})
#        except Appointment.DoesNotExist:
#            messages.error(request, "Invalid Booking ID.")
#            return render(request, "booking_cancellation/cancel_booking.html", {'error_message': "Invalid Booking ID."})
#    return render(request, "booking_cancellation/cancel_booking.html")


def send_otp_email(email, otp):
    subject = 'OTP for Booking Cancellation'
    message = f'Your OTP for booking cancellation is: {otp}'
    from_email = 'sandeep@godbms.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)


def view_appointment(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        try:
            appointment = Appointment.objects.get(booking_id=booking_id)
            otp = generate_otp()
            request.session['otp'] = otp
            request.session["booking_id"] = booking_id
            send_otp_email(appointment.email, otp)
            return redirect('verify_otp')
        except ObjectDoesNotExist:
            messages.error(request, "Invalid Booking ID.")
            return render(request, "booking_cancellation/cancel_booking.html", {'error_message': "Invalid Booking ID."})
    return render(request, "booking_cancellation/cancel_booking.html")


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get('otp')
        booking_id = request.session.get("booking_id")
        if entered_otp == stored_otp:
            appointment = Appointment.objects.get(booking_id=booking_id)
            del request.session['otp']  # Remove OTP from session after successful verification
            # Redirect to a success page or render the appointment details page for cancellation
            return render(request, 'booking_cancellation/view_appointment.html', {'appointment': appointment})
        else:
            messages.error(request, "Invalid OTP. Please try again.")
    return render(request, 'booking_cancellation/verify_otp.html')


def terms(request):
    return render(request, "other/terms&conditions.html")


def privacy(request):
    return render(request, "other/privacy_policy.html")


def refund(request):
    return render(request, "other/refund.html")


def form1(request):
    return render(request, "contract_forms/emergency_pet_transport.html")


def form2(request):
    return render(request, "contract_forms/pet_transportation_payment.html")


def form3(request):
    return render(request, "contract_forms/pet_transportation_service.html")


def extract_text_from_html(html_content):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text(separator='\n', strip=True)
    return text


def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="agreement.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw the agreement content
    agreement_text = request.POST.get('agreement_text')
    # Draw agreement_text using p.drawString() or other canvas methods

    # Draw the user's signature
    signature_data = request.POST.get('signature')
    # Decode the signature data URL and draw it on the PDF

    # Save the PDF file
    p.showPage()
    p.save()
    return response