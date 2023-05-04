from django.contrib import admin

# Register your models here.
from .models import School,Posts

class SchoolAdmin(admin.ModelAdmin):
    list_display = ('user', 'status')

admin.site.register(School, SchoolAdmin)


class UserPost(admin.ModelAdmin):
    list_display = ('id', 'user')

admin.site.register(Posts, UserPost)