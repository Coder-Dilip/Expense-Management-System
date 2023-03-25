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
    path("view-school-form/",views.school_form_list)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)