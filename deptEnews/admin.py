from django.contrib import admin
from .models import Department,Newsletter,Subscriber,Employee,Event,Announcement
from django.urls import reverse
from django.shortcuts import redirect
# Register your models here.

class YourNewsletterAdmin(admin.ModelAdmin):
    exclude = ('history',)

admin.site.register(Department)
admin.site.register(Subscriber)
admin.site.register(Newsletter,YourNewsletterAdmin)
admin.site.register(Event)
admin.site.register(Employee)
admin.site.register(Announcement)