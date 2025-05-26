from django.shortcuts import render, redirect
from .forms import ProfileRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
import json

from .forms import EmailAuthenticationForm
from .helper import get_form_errors
from .models import Profile


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('upload')

    context = {
        'error': ''
    }

    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)

            if user:
                login(request, user)

                next_url = request.GET.get('next', 'upload')

                return redirect(next_url)
            else:
                context['error'] = 'Email or password is wrong!'
        else:
            print(form.errors)
            context['error'] = get_form_errors(form)
    else:
        form = EmailAuthenticationForm()

    context['form'] = form

    return render(request, 'authentication/login.html', context)


def register(request):
    context = {}
    if request.method == "POST":
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("upload")
        else:
            context['error'] = get_form_errors(form)
    else:
        form = ProfileRegistrationForm()
    
    context['form'] = form
    
    return render(request, "authentication/register.html", context)


def sign_out(request):
    logout(request)
    return redirect('login')


def reset_password_page(request):
    context = {}
    uid = request.GET.get("uid")
    token = request.GET.get("token")

    uid = force_str(urlsafe_base64_decode(uid))
    user = Profile.objects.get(pk=uid)
    if not default_token_generator.check_token(user, token):
        context['error'] = "Token Expired"

    return render(request, "authentication/password_reset.html", context=context)


def forget_password_page(request):
    return render(request, "authentication/forget_password.html")


@csrf_exempt
def password_reset_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        try:
            user = Profile.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(f"/user/reset/?uid={uid}&token={token}")
            send_mail(
                "Reset your password",
                f"Click the link to reset your password: {reset_link}",
                "noreply@example.com",
                [email],
            )
            return JsonResponse({"status": "ok", "message": "Reset email sent"})
        except Profile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Email not found"}, status=404)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)


@csrf_exempt
def password_reset_api_confirm(request):
    if request.method == "POST":
        uid = request.POST.get("uid")
        token = request.POST.get("token")
        new_password = request.POST.get("new_password")

        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = Profile.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.is_active = True
                user.save()
                return JsonResponse({"status": "ok", "message": "Password reset successful"}, status=200)
            else:
                return JsonResponse({"status": "error", "message": "Invalid token"}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)
