from django.contrib import admin
from django.urls import path,include,re_path
from . import views
urlpatterns = [
    path("admin-dashboard/",views.index),
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path("admin-dashboard/profile",views.profile),
    path("admin-dashboard/icons",views.icons),
    path("admin-dashboard/table",views.table),
    path('logout/',views.logOut),
]