from django.db import models

# --------------------
# Model for Jobs
# --------------------
class Job(models.Model):
    job_id = models.IntegerField(unique=True)
    add_date = models.DateTimeField(null=True, blank=True)
    add_user_id = models.IntegerField(null=True, blank=True)
    cancel_date = models.DateField(null=True, blank=True)
    contract_amount = models.FloatField(null=True, blank=True)
    job_value = models.FloatField(null=True, blank=True)
    hs_object_id = models.IntegerField(null=True, blank=True)
    hubspot_createdate = models.DateTimeField(null=True, blank=True)
    hubspot_lastmodifieddate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Job {self.job_id}"


# --------------------
# Model for Divisions
# --------------------
class Division(models.Model):
    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    group_id = models.IntegerField(null=True, blank=True)
    is_corp = models.IntegerField(null=True, blank=True)
    is_inactive = models.IntegerField(null=True, blank=True)
    hs_object_id = models.IntegerField(null=True, blank=True)
    hubspot_createdate = models.DateTimeField(null=True, blank=True)
    hubspot_lastmodifieddate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Division {self.id}"


# --------------------
# Model for Employees
# --------------------
class Employee(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    employee_division_id = models.IntegerField(null=True, blank=True)
    employee_title_id = models.IntegerField(null=True, blank=True)
    hs_object_id = models.IntegerField(null=True, blank=True, unique=True)
    hubspot_createdate = models.DateTimeField(null=True, blank=True)
    hubspot_lastmodifieddate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Employee {self.firstname} {self.lastname or ''}"
    

class HubSpotSyncHistory(models.Model):
    endpoint = models.CharField(max_length=100, unique=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.endpoint} last synced at {self.last_synced_at}"

