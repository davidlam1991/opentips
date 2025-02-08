from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get("email")
        valid_domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "icloud.com", "aol.com"]
        domain = email.split('@')[-1]

        if domain not in valid_domains:
            raise ValidationError("Please use a valid email address from one of the following domains: " + ', '.join(valid_domains))

        return email

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password1", "password2"]


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={
            "placeholder": "Enter email"}),
    )

    def save(self, *args, **kwargs):
        User = get_user_model()
        email = self.cleaned_data['email']
        try:
            user = User.objects.get(email=email)
            kwargs['extra_email_context'] = {'username': user.username}
        except User.DoesNotExist:
            raise ValidationError("This email is not registered.")

        return super().save(*args, **kwargs)


class EmailChangeForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"placeholder": "New email", "class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = ["email"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("instance")
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if email == self.user.email:
            raise ValidationError("The new email cannot be the same as the old email.")

        valid_domains = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "icloud.com", "aol.com"]
        domain = email.split('@')[-1]

        if domain not in valid_domains:
            raise ValidationError("Please use a valid email address from one of the following domains: " + ', '.join(valid_domains))

        return email


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Current password", "class": "form-control"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "New password", "class": "form-control"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm new password", "class": "form-control"})
    )


