from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .forms import CustomPasswordResetForm

urlpatterns = [
    path("signup", views.user_signup, name="users-signup"),
    path("login", views.user_signin, name="users-login"),
    path("profile", views.profile, name="profile"),
    path("logout", views.user_logout, name="users-logout"),
    path("verify-email/<str:verification_token>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),

    path("password-reset", views.CustomPasswordResetView.as_view(
        template_name="users/password-reset.html",
        form_class=CustomPasswordResetForm), name="password-reset"),
    path("password-reset-done", auth_views.PasswordResetDoneView.as_view(
        template_name="users/password-reset-done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(
        template_name="users/password-reset-confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete", auth_views.PasswordResetCompleteView.as_view(
        template_name="users/password-reset-complete.html"), name="password_reset_complete"),
]