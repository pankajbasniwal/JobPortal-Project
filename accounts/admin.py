
from django.contrib import admin
from .models import StudentProfile, Company, UserProfile

admin.site.register(UserProfile)
admin.site.register(StudentProfile)
admin.site.register(Company)
