from django.db import models

class HubSpotData(models.Model):
    endpoint = models.CharField(max_length=100)
    record_id = models.CharField(max_length=100)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("endpoint", "record_id")
        verbose_name = "HubSpot Data"
        verbose_name_plural = "HubSpot Data"

    def __str__(self):
        return f"{self.endpoint} - {self.record_id}"


class HubSpotSyncHistory(models.Model):
    endpoint = models.CharField(max_length=100, unique=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.endpoint} last synced at {self.last_synced_at}"


# -------------------------------------------------------------------
# Model for the "jobs" endpoint (from your previous mapping)
# -------------------------------------------------------------------

class Job(models.Model):
    # "job_id" is required and unique.
    job_id = models.BigIntegerField(primary_key=True)

    accrued_commission_payout = models.FloatField(null=True, blank=True)
    add_date = models.DateTimeField(null=True, blank=True)
    add_user_id = models.BigIntegerField(null=True, blank=True)
    cancel_date = models.DateField(null=True, blank=True)
    cancel_reason_id = models.FloatField(null=True, blank=True)
    cancel_user_id = models.BigIntegerField(null=True, blank=True)
    client_cid = models.FloatField(null=True, blank=True)
    coc_sent_by = models.CharField(max_length=255, null=True, blank=True)
    coc_sent_on = models.DateField(null=True, blank=True)
    cogs_report_month = models.CharField(max_length=255, null=True, blank=True)
    commission_payout = models.FloatField(null=True, blank=True)
    company_cam_link = models.CharField(max_length=255, null=True, blank=True)
    contract_amount = models.FloatField(null=True, blank=True)
    contract_amount_difference = models.CharField(max_length=255, null=True, blank=True)
    contract_date = models.DateField(null=True, blank=True)
    contract_file_id = models.CharField(max_length=255, null=True, blank=True)
    contract_hours = models.FloatField(null=True, blank=True)
    contract_number = models.CharField(max_length=255, null=True, blank=True)
    deadline_date = models.DateField(null=True, blank=True)
    deposit_amount = models.FloatField(null=True, blank=True)
    deposit_type_id = models.FloatField(null=True, blank=True)
    division_id = models.FloatField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    estimate_job_duration = models.CharField(max_length=255, null=True, blank=True)
    finish_date = models.DateField(null=True, blank=True)
    forecast_month = models.CharField(max_length=255, null=True, blank=True)
    hoa = models.CharField(max_length=255, null=True, blank=True)
    hoa_approved = models.CharField(max_length=255, null=True, blank=True)
    hs_all_accessible_team_ids = models.JSONField(null=True, blank=True)
    hs_all_assigned_business_unit_ids = models.JSONField(null=True, blank=True)
    hs_all_owner_ids = models.JSONField(null=True, blank=True)
    hs_all_team_ids = models.JSONField(null=True, blank=True)
    hs_created_by_user_id = models.BigIntegerField(null=True, blank=True)
    hs_createdate = models.DateTimeField(null=True, blank=True)
    hs_lastmodifieddate = models.DateTimeField(null=True, blank=True)
    hs_merged_object_ids = models.JSONField(null=True, blank=True)
    hs_object_id = models.BigIntegerField(null=True, blank=True)
    hs_object_source = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_1 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_2 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_3 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_id = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_label = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_user_id = models.BigIntegerField(null=True, blank=True)
    hs_pinned_engagement_id = models.BigIntegerField(null=True, blank=True)
    hs_read_only = models.BooleanField(null=True, blank=True)
    hs_shared_team_ids = models.JSONField(null=True, blank=True)
    hs_shared_user_ids = models.JSONField(null=True, blank=True)
    hs_unique_creation_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    hs_updated_by_user_id = models.BigIntegerField(null=True, blank=True)
    hs_user_ids_of_all_notification_followers = models.JSONField(null=True, blank=True)
    hs_user_ids_of_all_notification_unfollowers = models.JSONField(null=True, blank=True)
    hs_user_ids_of_all_owners = models.JSONField(null=True, blank=True)
    hs_was_imported = models.BooleanField(null=True, blank=True)
    hubspot_owner_id = models.BigIntegerField(null=True, blank=True)
    hubspot_team_id = models.BigIntegerField(null=True, blank=True)
    install_date = models.DateField(null=True, blank=True)
    install_time = models.CharField(max_length=255, null=True, blank=True)
    install_time_format = models.FloatField(null=True, blank=True)
    is_cogs_report_month_updated = models.FloatField(null=True, blank=True)
    is_company_cam = models.CharField(max_length=255, null=True, blank=True)
    is_earned_not_paid = models.FloatField(null=True, blank=True)
    is_financing = models.FloatField(null=True, blank=True)
    is_five_star_review = models.CharField(max_length=255, null=True, blank=True)
    is_in_progress = models.FloatField(null=True, blank=True)
    is_lead_pb = models.FloatField(null=True, blank=True)
    is_payment_finalized = models.CharField(max_length=255, null=True, blank=True)
    is_refund = models.FloatField(null=True, blank=True)
    is_reviewed = models.FloatField(null=True, blank=True)
    is_sales_tax_exempt = models.FloatField(null=True, blank=True)
    payment_amount = models.FloatField(null=True, blank=True)
    payment_not_finalized_reason = models.CharField(max_length=255, null=True, blank=True)
    payment_type = models.CharField(max_length=255, null=True, blank=True)
    pm_finished_on = models.DateField(null=True, blank=True)
    pp_id_updated = models.FloatField(null=True, blank=True)
    prep_issue_id = models.CharField(max_length=255, null=True, blank=True)
    prep_status_id = models.FloatField(null=True, blank=True)
    prep_status_is_reset = models.FloatField(null=True, blank=True)
    prep_status_notes = models.TextField(null=True, blank=True)
    prep_status_set_date = models.DateTimeField(null=True, blank=True)
    price_level = models.CharField(max_length=255, null=True, blank=True)
    price_level_commission = models.FloatField(null=True, blank=True)
    price_level_commission_reduction = models.FloatField(null=True, blank=True)
    price_level_goal = models.FloatField(null=True, blank=True)
    production_month = models.FloatField(null=True, blank=True)
    production_user_id = models.FloatField(null=True, blank=True)
    project_coordinator_user_id = models.FloatField(null=True, blank=True)
    prospect_id = models.FloatField(null=True, blank=True)
    ready_date = models.DateField(null=True, blank=True)
    ready_status = models.FloatField(null=True, blank=True)
    reasons_other = models.CharField(max_length=255, null=True, blank=True)
    refund_date = models.DateField(null=True, blank=True)
    refund_user_id = models.FloatField(null=True, blank=True)
    reviewed_by = models.CharField(max_length=255, null=True, blank=True)
    sales_tax_rate = models.FloatField(null=True, blank=True)
    service_id = models.FloatField(null=True, blank=True)
    sold_date = models.DateField(null=True, blank=True)
    sold_user_id = models.FloatField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    start_month_old = models.FloatField(null=True, blank=True)
    start_request_date = models.DateField(null=True, blank=True)
    status = models.FloatField(null=True, blank=True)
    subcontractor_confirmed = models.FloatField(null=True, blank=True)
    subcontractor_id = models.FloatField(null=True, blank=True)
    subcontractor_status_id = models.FloatField(null=True, blank=True)
    time_format = models.FloatField(null=True, blank=True)
    user_id = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.job_id)


# -------------------------------------------------------------------
# Model for the "divisions" endpoint (from your previous mapping)
# -------------------------------------------------------------------

class Division(models.Model):
    # The mapping defines "id" as required and unique.
    id = models.BigIntegerField(primary_key=True)
    
    abbreviation = models.CharField(max_length=255, null=True, blank=True)
    group_id = models.BigIntegerField(null=True, blank=True)
    
    hs_all_accessible_team_ids = models.JSONField(null=True, blank=True)
    hs_all_assigned_business_unit_ids = models.JSONField(null=True, blank=True)
    hs_all_owner_ids = models.JSONField(null=True, blank=True)
    hs_all_team_ids = models.JSONField(null=True, blank=True)
    
    hs_created_by_user_id = models.BigIntegerField(null=True, blank=True)
    hs_createdate = models.DateTimeField(null=True, blank=True)
    hs_lastmodifieddate = models.DateTimeField(null=True, blank=True)
    hs_merged_object_ids = models.JSONField(null=True, blank=True)
    hs_object_id = models.BigIntegerField(null=True, blank=True)
    
    hs_object_source = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_1 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_2 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_detail_3 = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_id = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_label = models.CharField(max_length=255, null=True, blank=True)
    hs_object_source_user_id = models.BigIntegerField(null=True, blank=True)
    
    hs_pinned_engagement_id = models.BigIntegerField(null=True, blank=True)
    hs_read_only = models.BooleanField(null=True, blank=True)
    hs_shared_team_ids = models.JSONField(null=True, blank=True)
    hs_shared_user_ids = models.JSONField(null=True, blank=True)
    hs_unique_creation_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    hs_updated_by_user_id = models.BigIntegerField(null=True, blank=True)
    hs_user_ids_of_all_notification_followers = models.JSONField(null=True, blank=True)
    hs_user_ids_of_all_notification_unfollowers = models.JSONField(null=True, blank=True)
    
    hs_was_imported = models.BooleanField(null=True, blank=True)
    hubspot_owner_assigneddate = models.DateTimeField(null=True, blank=True)
    hubspot_owner_id = models.BigIntegerField(null=True, blank=True)
    hubspot_team_id = models.BigIntegerField(null=True, blank=True)
    
    # Specific division properties
    is_corp = models.FloatField(null=True, blank=True)
    is_inactive = models.FloatField(null=True, blank=True)
    is_omniscient = models.FloatField(null=True, blank=True)
    is_utility = models.FloatField(null=True, blank=True)
    is_vp_commission_ignored = models.FloatField(null=True, blank=True)
    label = models.CharField(max_length=255, null=True, blank=True)
    paychex_company_number = models.CharField(max_length=255, null=True, blank=True)
    region_id = models.BigIntegerField(null=True, blank=True)
    rescission_period_days = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.id)


# -------------------------------------------------------------------
# New Model for the "employees" endpoint based on your mapping
# -------------------------------------------------------------------

class Employee(models.Model):
    # Although the mapping’s required property is "firstname",
    # HubSpot records will include a unique record ID (hs_object_id)
    # which we store as unique.
    hs_object_id = models.BigIntegerField(unique=True, null=True, blank=True)

    add_date_time = models.DateTimeField(null=True, blank=True)
    add_user_id = models.CharField(max_length=255, null=True, blank=True)
    advance_account_id = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    employee_division_id = models.BigIntegerField(null=True, blank=True)
    employee_title_id = models.BigIntegerField(null=True, blank=True)
    employee_user_id = models.BigIntegerField(null=True, blank=True)

    firstname = models.CharField(max_length=255)  # required per mapping
    gender_id = models.BigIntegerField(null=True, blank=True)
    google_calender_channel_expiration = models.CharField(max_length=255, null=True, blank=True)
    google_calender_channel_id = models.CharField(max_length=255, null=True, blank=True)
    google_calender_last_sync = models.CharField(max_length=255, null=True, blank=True)
    google_calender_resource_id = models.CharField(max_length=255, null=True, blank=True)
    google_calender_sync_start = models.CharField(max_length=255, null=True, blank=True)

    hs_pinned_engagement_id = models.BigIntegerField(null=True, blank=True)
    hs_read_only = models.BooleanField(null=True, blank=True)
    hs_shared_team_ids = models.JSONField(null=True, blank=True)
    hs_shared_user_ids = models.JSONField(null=True, blank=True)
    hs_unique_creation_key = models.CharField(max_length=255, unique=True, null=True, blank=True)
    hs_updated_by_user_id = models.BigIntegerField(null=True, blank=True)
    hs_user_ids_of_all_notification_followers = models.JSONField(null=True, blank=True)
    hs_user_ids_of_all_notification_unfollowers = models.JSONField(null=True, blank=True)
    hs_user_ids_of_all_owners = models.JSONField(null=True, blank=True)
    hs_was_imported = models.BooleanField(null=True, blank=True)

    hubspot_owner_assigneddate = models.DateTimeField(null=True, blank=True)
    hubspot_owner_id = models.BigIntegerField(null=True, blank=True)
    hubspot_team_id = models.BigIntegerField(null=True, blank=True)

    inactive_on = models.DateTimeField(null=True, blank=True)
    inactive_reason_id = models.CharField(max_length=255, null=True, blank=True)
    inactive_reason_other = models.CharField(max_length=255, null=True, blank=True)
    inactive_transfer_division_id = models.CharField(max_length=255, null=True, blank=True)
    is_inactive = models.CharField(max_length=255, null=True, blank=True)

    lead_call_center = models.CharField(max_length=255, null=True, blank=True)
    lead_radius_distance = models.CharField(max_length=255, null=True, blank=True)
    lead_radius_zip = models.CharField(max_length=255, null=True, blank=True)
    lead_type = models.CharField(max_length=255, null=True, blank=True)
    lead_views_allowed = models.CharField(max_length=255, null=True, blank=True)

    lastname = models.CharField(max_length=255, null=True, blank=True)
    manager_user_id = models.BigIntegerField(null=True, blank=True)
    project_commission_pct = models.CharField(max_length=255, null=True, blank=True)
    timezone_name = models.CharField(max_length=255, null=True, blank=True)
    user_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.firstname
