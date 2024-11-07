from django import forms


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)