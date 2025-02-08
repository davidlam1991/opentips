from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView

from .forms import SignUpForm, EmailChangeForm, CustomPasswordChangeForm, CustomPasswordResetForm
from .models import OtpToken
from posts.models import Post, Comment

# Create your views here.


def user_signup(request):
    form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! A code was sent to your Email")

            otp = OtpToken.objects.filter(user=user).last()
            # return redirect("post-main-page")
            return redirect("verify-email", verification_token=otp.verification_token)
        else:
            errors = form.errors.as_data().get('password2', [])
            for error in errors:
                for message in error.messages:
                    messages.warning(request, message)

    context = {"signup_form": form}

    return render(request, "users/signup.html", context)


def verify_email(request, verification_token):
    # user = get_user_model().objects.get(username=username)
    # user_otp = OtpToken.objects.filter(user=user).last()
    otp = get_object_or_404(OtpToken, verification_token=verification_token)
    user = otp.user

    if request.method == "POST":
        if otp.otp_code == request.POST['otp_code']:
            # user_otp.verify_otp_code(request.POST['otp_code'])
            if otp.otp_expires_at > timezone.now():
                user.is_active = True

                # Get the new email from the session
                new_email = request.session.pop('new_email', None)

                if new_email:
                    user.email = new_email
                    messages.success(request, "Your email has been verified and updated!")
                else:
                    messages.success(request, "Account activated successfully!! You can Login now.")

                user.save()
                return redirect("users-login")
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", verification_token=otp.verification_token)
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", verification_token=otp.verification_token)

    context = {"user": user}
    return render(request, "users/verify-token.html", context)


def resend_otp(request):
    if request.method == "POST":
        user_email = request.POST["otp_email"]
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

            # email variables
            subject = "Email Verification"
            message = f"""
            Hi {user.username}, here is your code "{otp.otp_code}"
            it expires in 5 minute, use the url below to redirect back to the website
            https://127.0.0.1:8000/users/verify-email/{otp.verification_token}
            """
            sender = "open.tips.forum@gmail.com"
            receiver = [user.email, ]

            send_mail(
                subject,
                message,
                sender,
                receiver,
                fail_silently=False,
            )

            messages.success(request, "A new code has been sent to your email")
            return redirect("verify-email", username=user.username)
        else:
            messages.warning(request, "This email doesn't exist")
            return redirect("resend-otp")

    context = {}
    return render(request, "users/resend-otp.html", context)


def user_signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Hi {request.user.username}, you are now logged in")
            return redirect("post-main-page")
        else:
            messages.warning(request, "Invalid username or password")
            return render(request, "users/login.html")

    return render(request, "users/login.html")


def user_logout(request):
    auth.logout(request)
    messages.warning(request, "You are logged out")

    return redirect("post-main-page")


@login_required(login_url="users-login")
def profile(request):
    user = request.user
    user_reviews = Post.objects.filter(creator=user).order_by("-date", "-release_date")
    user_comments = Comment.objects.filter(author=user).order_by("-date_posted")

    if request.method == "POST":
        email_form = EmailChangeForm(request.POST, instance=user)
        password_form = CustomPasswordChangeForm(user, request.POST)

        if 'current_password' in request.POST:
            current_password = request.POST.get('current_password')
            authenticated_user = authenticate(username=user.username, password=current_password)

            if authenticated_user is not None:
                if email_form.is_valid():
                    new_email = email_form.cleaned_data['email']
                    user.is_active = False
                    user.save()

                    request.session['new_email'] = new_email

                    otp = OtpToken.objects.create(user=user,
                                                  otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))

                    subject = "Email Verification"
                    message = f"""
                                Hi {user.username}, here is your code "{otp.otp_code}"
                                It expires in 5 minutes. Please use this link to verify your email:
                                https://127.0.0.1:8000/users/verify-email/{otp.verification_token}
                                """
                    sender = "open.tips.forum@gmail.com"
                    receiver = [new_email]

                    send_mail(subject, message, sender, receiver, fail_silently=False)

                    messages.success(request, "A verification has been sent to your new email address.")
                    return redirect("verify-email", username=user.username)
                else:
                    messages.warning(request, "Please enter a valid email address.")
            else:
                messages.warning(request, "Incorrect password. Please try again.")

        if 'old_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been updated.")
                return redirect("profile")
            else:
                for field, errors in password_form.errors.items():
                    for error in errors:
                        messages.warning(request, error)
    else:
        email_form = EmailChangeForm(instance=user)
        password_form = CustomPasswordChangeForm(user)

    context = {
        "email_form": email_form,
        "password_form": password_form,
        "user": user,
        "user_reviews": user_reviews,
        "user_comments": user_comments,
    }

    return render(request, "users/profile.html", context)


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    email_template_name = 'registration/password_reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = 'localhost:8000'
        context['protocol'] = 'https'
        return context


