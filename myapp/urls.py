from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
    path("blog/", views.blog, name="blog"),
    path("price/", views.price, name="price"),
    path("service/", views.service, name="service"),
    path("team/", views.team, name="team"),
    path("testimonial/", views.testimonial, name="testimonial"),
    path("booking/", views.booking, name="booking"),
    path("contact/", views.contact, name="contact"),
    path("appointment-summary/", views.summary, name="summary"),
    path("save-appointment/", views.save_appointment, name="save"),
    path("success/<str:booking_id>/", views.success, name="success"),
    path("download-pdf/<str:booking_id>/", views.download_pdf, name='download_pdf'),
    path("print/", views.print, name="print"),
    path('cancel-booking/', views.view_appointment, name='view_appointment'),
    path('cancel-booking/cancel/', views.cancel_booking, name='cancel_booking'),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("terms&conditions/", views.terms, name="terms&conditions"),
    path("privacy-policy/", views.privacy, name="privacy"),
    path("refund/", views.refund, name="refund"),
    path("form1/", views.form1, name="form1"),
    path("form2/", views.form2, name="form2"),
    path("form3/", views.form3, name="form3"),
    path("agreement/", views.agreement, name="agreement"),
    path("", include("admin.urls"))

]