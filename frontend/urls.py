from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path("",views.index),
path("login/",views.login_view),
path('register/',views.register_user),
path("contact/",views.contact),
path("forgot-password/",views.forgot_password),
path("forgot-password2/",views.forgot_password2),
path("forgot-password3/",views.forgot_password3)
]