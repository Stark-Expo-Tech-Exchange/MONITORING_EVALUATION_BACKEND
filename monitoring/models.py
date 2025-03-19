from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    groups = models.ManyToManyField(Group, related_name="monitoring_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="monitoring_user_permissions", blank=True)

    def __str__(self):
        return self.username

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Indicator(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="indicators")
    name = models.CharField(max_length=100)
    target_value = models.FloatField()
    actual_value = models.FloatField(default=0.0)
    last_updated = models.DateTimeField(auto_now=True)

class Report(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    report_date = models.DateField(auto_now_add=True)
    summary = models.TextField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE)
