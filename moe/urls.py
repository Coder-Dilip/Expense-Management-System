from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path("admin-dashboard/",views.index),
    path("admin-dashboard/profile",views.profile),
    path("admin-dashboard/icons",views.icons),
    path("admin-dashboard/table",views.table),
    path('logout/',views.logOut),
    path('admin-dashboard/to-distribute',views.school_budget_table),
    path('admin-dashboard/distribute/<username>',views.school_distribute),


    # verify school
    path("verify/<username>",views.verify_school),
    path("distribute-budget/<username>",views.distribute_budget),
    path("admin-dashboard/reports",views.school_reports),
     path('reports/', views.get_reports, name='get_reports'),
     path('report_detail/<id>', views.get_reports, name='report_detail'),
]




