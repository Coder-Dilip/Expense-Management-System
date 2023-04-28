from django.contrib import admin

# Register your models here.
from .models import SchoolForm,DailyTrack,SchoolBudget

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','name','contact_email')

admin.site.register(SchoolForm, SchoolAdmin)


class DailyTracking(admin.ModelAdmin):
    list_display=('id','school_username','school_items','food')
admin.site.register(DailyTrack,DailyTracking)

class SchoolBudgeting(admin.ModelAdmin):
    list_display=('id','school_username','distributed')
admin.site.register(SchoolBudget,SchoolBudgeting)