from django.contrib import admin
from .models import Job, Division, Employee
# Optionally register your models in the admin:

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("job_id", "job_value")
    search_fields = ("job_id",)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ("id", "abbreviation")
    search_fields = ("id", "abbreviation")

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "email")
    search_fields = ("firstname", "lastname", "email")
