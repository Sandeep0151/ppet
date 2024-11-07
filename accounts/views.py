from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .utils import send_reset_password_email
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .forms import ForgotPasswordForm, ResetPasswordForm


def login_page(request):
    if request.method == "POST":
        username_or_email = request.POST.get("username_or_email")
        password = request.POST.get("password")

        # Check if the input is a valid email address
        if '@' in username_or_email:
            # Authenticate user using email and password
            user = authenticate(request, email=username_or_email, password=password)
        else:
            # Authenticate user using username and password
            user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            messages.info(request, "Invalid Username or Password")
            return redirect("login")

        else:
            login(request, user)
            messages.info(request, "Login Successfully")
            return redirect("login")

    return render(request, "user/login.html")


def logout_page(request):
    logout(request)
    return redirect("login")


def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.info(request, "Email Already Taken.")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.info(request, "Username Already Taken.")
            return redirect("register")

        # Create user without username field
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
        )
        user.set_password(password)
        user.save()
        messages.info(request, "Account Created Successfully.")
        return redirect("register")
    return render(request, "user/register.html")


def send_forget_password_mail(email, token):
    subject = 'Password Reset Request'
    message = f'Click the following link to reset your password: http://192.168.0.247:8000/change-password/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def reset_password(request, token):
    try:
        profile = Profile.objects.get(forgot_password_token=token)
        user = profile.user
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                user.set_password(new_password)
                user.save()
                profile.forgot_password_token = ''
                profile.save()
                messages.success(request, 'Password reset successfully. You can now log in with your new password.')
                return redirect('login')
        else:
            form = ResetPasswordForm()
        return render(request, 'user/reset_password.html', {'form': form})
    except Profile.DoesNotExist:
        messages.error(request, 'Invalid reset password link.')
        return redirect('login')


def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                send_reset_password_email(user)
                messages.success(request, 'Password reset email sent successfully.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'Invalid email address.')
    else:
        form = ForgotPasswordForm()
    return render(request, 'user/forgot_password.html', {'form': form})


