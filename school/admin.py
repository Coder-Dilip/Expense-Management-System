from django.contrib import admin

# Register your models here.
from .models import Automate, DailySavingPlan, MonthlySavingPlan, SchoolForm,DailyTrack,SchoolBudget, DailySaving, Report

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('id','username','email','name','contact_email')

admin.site.register(SchoolForm, SchoolAdmin)


class DailyTracking(admin.ModelAdmin):
    list_display=('id','school_username','school_items','food')
admin.site.register(DailyTrack,DailyTracking)

class SchoolBudgeting(admin.ModelAdmin):
    list_display=('id','school_username','curr_date','distributed')
admin.site.register(SchoolBudget,SchoolBudgeting)

class saveMonthlyDistribute(admin.ModelAdmin):
    list_display=(id,'school_username','school_items')
admin.site.register(MonthlySavingPlan,saveMonthlyDistribute)

class saveDailyDistribute(admin.ModelAdmin):
    list_display=(id,'school_username','school_items')
admin.site.register(DailySavingPlan,saveDailyDistribute)


class DayToDaySaving(admin.ModelAdmin):
        list_display=(id,'school_username','school_items')
admin.site.register(DailySaving,DayToDaySaving)


class Reporting(admin.ModelAdmin):
        list_display=(id,'school_username','curr_date')
admin.site.register(Report,Reporting)


class Automating(admin.ModelAdmin):
     list_display=(id,'school_username','sheet_url')
admin.site.register(Automate,Automating)
