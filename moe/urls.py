from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path("admin-dashboard/",views.index),
    path("admin-dashboard/profile",views.profile),
    path("admin-dashboard/icons",views.icons),
    path("admin-dashboard/table",views.table),
    path('logout/',views.logOut),



    # verify school
    path("verify/<username>",views.verify_school)
     
]




