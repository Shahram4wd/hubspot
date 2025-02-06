from django.contrib import admin
from .models import HubSpotData, HubSpotSyncHistory, Job, Division, Employee

@admin.register(HubSpotData)
class HubSpotDataAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'record_id', 'created_at', 'updated_at')
    search_fields = ('endpoint', 'record_id')
    list_filter = ('endpoint',)

@admin.register(HubSpotSyncHistory)
class HubSpotSyncHistoryAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'last_synced_at')
    search_fields = ('endpoint',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    # Removed 'updated_at' from list_display since Job does not define it.
    list_display = ('job_id', 'contract_number', 'add_date')
    search_fields = ('job_id', 'contract_number')
    list_filter = ('add_date',)

@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('id', 'abbreviation', 'group_id', 'label')
    search_fields = ('id', 'abbreviation', 'label')
    list_filter = ('group_id',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('hs_object_id', 'firstname', 'lastname', 'email', 'employee_user_id')
    search_fields = ('hs_object_id', 'firstname', 'lastname', 'email')
    list_filter = ('employee_division_id',)
