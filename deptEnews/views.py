from django.shortcuts import render,redirect,get_object_or_404
from .models import Subscriber, Newsletter,Department,Event,Announcement,Employee
from .forms import NewsletterForm,EmployeeSpotlightForm,EventForm,AnnouncementForm
from django.core.mail import send_mail
from django.utils import timezone 
from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to the home page after successful login
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login') 

def is_editor(user):
    return user.groups.filter(name='Editors').exists()

# Create your views here.
def home(request):
    # Get the latest newsletters and upcoming events
    departments = Department.objects.all()
    latest_newsletters = Newsletter.objects.order_by('-issue_date')[:3]
    upcoming_events = Event.objects.filter()[:3]

    context = {
        'latest_newsletters': latest_newsletters,
        'upcoming_events': upcoming_events,
        'departments': departments,
    }
    return render(request, 'home.html', context)


def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        department_name = request.POST.get('department')  # Assuming you're using department name as the value
        print(department_name)
        department = Department.objects.get(name=department_name)
        subscriber, created = Subscriber.objects.get_or_create(em=email, department=department)
        if created:
            subscriber.save()
            messages.success(request,'Subscription Successful')
            # Optionally send a confirmation email
            return redirect('subscribe')
    departments = Department.objects.all() 
    return render(request, 'subscribe.html', {'departments': departments})

# View to create a newsletter (accessible only to editors)
@user_passes_test(is_editor)
def create_newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter=form.save(commit=False)
            department=form.cleaned_data['department']
            title=form.cleaned_data['title']
            desc=form.cleaned_data['desc']
            announcement= form.cleaned_data['announcement']
            employee = form.cleaned_data['employee']
            event= form.cleaned_data['event']
             # Get subscribers for the specified department
            subscribers = Subscriber.objects.filter(department=department)
            for subscriber in subscribers:
                send_mail(
                    subject=title,
                    message=desc,
                    from_email='shambstar@egmail.com',
                    recipient_list=[subscriber.em],  # Use subscriber's email
                    fail_silently=False,
                )
            newsletter.save()
            newsletter.announcement.set(announcement)
            newsletter.employee.set(employee)
            newsletter.event.set(event)
            
            messages.success(request,'Newsletter Creation and Mailing Successful')
            return redirect('create_newsletter')
    else:
        form = NewsletterForm()
        if not request.user.groups.filter(name='Editors').exists():  # Check for editor group
            raise PermissionDenied("You are not authorized to create newsletters. Please contact an editor for assistance.")
    return render(request, 'create_newsletter.html', {'form': form})

def newsletter_by_department(request, department_name):
    department_newsletters = Newsletter.objects.filter(department__name=department_name)
    return render(request, 'newsletter_by_department.html', {'department': department_name, 'newsletters': department_newsletters})

def newsletter_detail(request,department_name,newsletter_title):
    newsletter = get_object_or_404(Newsletter, department__name=department_name, title=newsletter_title)
    return render(request, 'newsletter_detail.html', {'newsletter': newsletter})

@user_passes_test(is_editor)
def create_employee_spotlight(request):
    if request.method == 'POST':
        form = EmployeeSpotlightForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Employee Spotlight Creation Successful')
            return redirect('create_employee_spotlight')
    else:
        form = EmployeeSpotlightForm()
    return render(request, 'employee_spotlight_form.html', {'form': form})

@user_passes_test(is_editor)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Announcement Creation Successful')
            return redirect('create_announcement')
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})

@user_passes_test(is_editor)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'EventCreation Successful')
            return redirect('create_event')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})
