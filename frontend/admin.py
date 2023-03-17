from django.contrib import admin

# Register your models here.
from .models import School

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')

admin.site.register(School, SchoolAdmin)