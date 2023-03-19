from django.shortcuts import render,redirect
from . import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import School
from django.contrib.auth.models import User
# Create your views here.

def index(request):
    return render(request,"frontend/index.html")

def login_view(request):
    form = forms.LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if School.objects.filter(user=user).exists():
                  return redirect('/shool-dashboard') # Redirect to home page
                else:
                    return redirect("/admin-dashboards")
                
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "frontend/home/login.html", {"form": form, "msg": msg})

def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            status = "new" # set default status
            answer = request.POST.get('security_question')
            School.objects.create(user=user, status=status,security_question="first word of the school if you want to rename your school",security_answer=answer)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True


        else:
            msg = 'Form is not valid'
    else:
        form = forms.SignUpForm()

    return render(request, "frontend/home/register.html", {"form": form, "msg": msg, "success": success})


def contact(request):
    return render(request, "frontend/home/contact.html")


def forgot_password(request):
    if request.method=="POST":
        username=request.POST.get('username')
        print("username")
        return redirect(f"/forgot-password2?key={username}")

    return render(request, "frontend/home/forgot_password.html")

def forgot_password2(request):
    if request.method=="POST":
        username=request.POST.get('username')
        answer=request.POST.get("answer")
        return redirect(f"/forgot-password3?key={username}")
    return render(request, "frontend/home/forgot_password2.html")

def forgot_password3(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get("password")
        user = User.objects.get(username=username)

    # Set the new password for the user

        user.set_password(password)

    # Save the user object to update the password in the database
        user.save()
        return redirect("/login")
    

    return render(request, "frontend/home/forgot_password3.html")