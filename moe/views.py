from django.shortcuts import render,redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

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


