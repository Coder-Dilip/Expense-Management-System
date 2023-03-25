from django.contrib import admin

# Register your models here.
from .models import SchoolForm

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','name','contact_email')

admin.site.register(SchoolForm, SchoolAdmin)