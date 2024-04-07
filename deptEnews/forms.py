from django import forms
from django.forms import inlineformset_factory
from .models import Newsletter,Department,Employee,Announcement,Event

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = Newsletter
        fields = ['title', 'issue_date', 'editor', 'desc', 'department','announcement','employee','event']

class EmployeeSpotlightForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'bio']

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content','date']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date','location','department'] 