from django.db import models

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=200)
    hod=models.CharField(max_length=100)
    site=models.URLField()


class Subscriber(models.Model):
    em=models.EmailField()
    name=models.CharField(max_length=100)
    sdate=models.DateTimeField(auto_now_add=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_subscribed = models.DateTimeField(auto_now_add=True)

class Announcement(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateField()

class Employee(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Event(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    date=models.DateTimeField()
    location=models.CharField(max_length=200)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)

class Newsletter(models.Model):
    title=models.CharField(max_length=100)
    issue_date=models.DateTimeField()
    editor=models.CharField(max_length=100)
    desc=models.TextField()
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    announcement=models.ManyToManyField(Announcement)
    employee=models.ManyToManyField(Employee)
    event=models.ManyToManyField(Event)