from django.shortcuts import render,redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from frontend.models import School
from school.models import SchoolForm
@login_required(login_url="/login/")
def index(request):
    return render(request,"moe/index.html")


def logOut(request):
    logout(request)
    return redirect("/")
    
@login_required(login_url="/login/")
def profile(request):
    return render(request,"moe/profile.html")

@login_required(login_url="/login/")
def icons(request):
    return render(request,"moe/icons.html")

@login_required(login_url="/login/")
def table(request):
    return render(request,"moe/tables.html")


@login_required(login_url="/login/")
def verify_school(request, username):
    current_logged_in=request.user
    if School.objects.filter(user=current_logged_in).exists():
        return redirect('/')
    else:
        school_form = SchoolForm.objects.get(username=username)
        usr=User.objects.get(username=username)
        school=School.objects.get(user=usr)
        school.status="old"
        school_form.status = 1
        school_form.save()
        school.save()
        return redirect('/admin-dashboard')



