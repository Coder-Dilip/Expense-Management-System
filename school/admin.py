from django.contrib import admin

# Register your models here.
from .models import DailySavingPlan, MonthlySavingPlan, SchoolForm,DailyTrack,SchoolBudget

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