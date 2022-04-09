from email import message
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect 
from .models import *
import uuid
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth import authenticate , login
# Create your views here.


def home(request):
    return render(request , 'home.html')

def login_main(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request , 'User not found')
            return redirect('login')
        profile_obj = MyUser.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request , 'Profile is not verifed')
            return redirect('login')
        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request , 'Wrong Password')
            return redirect('login')
        login(request , user)
        return redirect(game)
    return render(request , 'login.html')
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request , 'Username is already taken')
                return redirect('signup')
            if User.objects.filter(email=email).first():
                messages.success(request , 'Email is already in use')
                return redirect('signup')
            user_obj = User.objects.create(username=username , email= email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = MyUser.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            auth_email(email , auth_token)
            return redirect('token_send')
        except Exception as e:
            print(e)
    return render(request , 'signup.html')

def verify(request , auth_token):
    try:
        profile_obj = MyUser.objects.filter(auth_token=auth_token).first()
        if profile_obj:
            if profile_obj.is_verified:
                message.success(request , 'Your accunt is already verifed')
                return redirect('login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request , 'Your account has been verified')
            return redirect('login')
        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('game')

def success(request):
    return render(request , 'success.html')
@login_required
def game(request):
    return render(request , 'game.html')

def token_send(request):
    return render(request , 'token_send.html')

def error(request):
    return render(request , 'error.html')

def auth_email(email , token):
    subject = "Your Account is needed to be verified"
    message = f"Hi please click the below email for the authentication of your account http://127.0.0.1:8000/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject , message , email_from , recipient_list)
