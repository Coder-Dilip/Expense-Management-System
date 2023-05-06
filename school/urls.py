from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path("school-form/",views.school_form),
    path("success/",views.success),
    path("view-image/<username>",views.view_image),
    path("view-school/<username>",views.school_details),
    path("view-school-form/",views.school_form_list),
    path('school-dashboard',views.school_dashboard),
    path('school-dashboard/daily-track',views.daily_track),
    path('school-dashboard/stats/<username>',views.statistics),
    path('school-dashboard/automate',views.automate),
    path('school-dashboard/spendings',views.spendings),
    path('save_daily_saving_plan/', views.save_daily_saving_plan, name='save_daily_saving_plan'),
    path('school-dashboard/data-for-visualization',views.get_school_expenses),
    path('school-dashboard/saving-data-for-visualization',views.get_school_saving_expenses),
    path('school-dashboard/expected-spending-api',views.expected_spending_api),
    path('school-dashboard/expected-saving-api',views.expected_saving_api),
    path('school-dashboard/savings',views.savings),
    path('school-dashboard/reports',views.reports),
    path('dummy-letter/', views.dummy_letter, name='dummy_letter'),
    path('dummy-letter2/', views.dummy_letter2, name='dummy_letter'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



