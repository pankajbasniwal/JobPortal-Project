
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.user.username


class StudentProfile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    phone = models.CharField(max_length=15)

    education = models.CharField(max_length=100)

    skills = models.TextField()

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


class Company(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=150)

    description = models.TextField()

    website = models.URLField(blank=True)

    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name
