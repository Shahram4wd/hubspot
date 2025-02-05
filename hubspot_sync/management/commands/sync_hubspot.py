import asyncio
from datetime import datetime

import aiohttp
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from hubspot_sync.models import Job, Division, Employee

class Command(BaseCommand):
    help = "Sync data from HubSpot API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--endpoint",
            nargs="+",
            help="Specify one or more endpoints to sync. If omitted, endpoints will be discovered.",
        )
        parser.add_argument(
            "--concurent",
            type=int,
            default=5,
            help="Number of endpoints to process concurrently (default: 5).",
        )

    def handle(self, *args, **options):
        endpoints = options.get("endpoint")
        concurrent = options.get("concurent")
        token = settings.HUBSPOT_API_TOKEN

        if not token:
            raise CommandError("HUBSPOT_API_TOKEN is not set in settings or environment variables.")

        self.stdout.write(self.style.SUCCESS("Starting HubSpot sync..."))
        asyncio.run(self.async_handle(endpoints, concurrent, token))
        self.stdout.write(self.style.SUCCESS("HubSpot sync complete."))

    async def async_handle(self, endpoints, concurrent, token):
        semaphore = asyncio.Semaphore(concurrent)
        async with aiohttp.ClientSession() as session:
            if not endpoints:
                endpoints = await self.discover_endpoints(session, token)
                self.stdout.write(self.style.SUCCESS(f"Discovered endpoints: {endpoints}"))
            tasks = [self.sync_endpoint(ep, token, session, semaphore) for ep in endpoints]
            await asyncio.gather(*tasks)

    async def discover_endpoints(self, session, token):
        url = "https://api.hubapi.com/crm/v3/schemas"
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                self.stdout.write(self.style.ERROR(f"Failed to discover endpoints. Status: {response.status}"))
                return []
            data = await response.json()
        endpoints = [schema.get("name") for schema in data.get("results", []) if schema.get("name")]
        return endpoints

    async def sync_endpoint(self, endpoint, token, session, semaphore):
        async with semaphore:
            self.stdout.write(self.style.SUCCESS(f"Syncing endpoint: {endpoint}"))
            last_sync = await sync_to_async(self.get_last_sync)(endpoint)
            params = {}
            if last_sync:
                params["updatedAfter"] = last_sync.isoformat()
            url = f"https://api.hubapi.com/crm/v3/objects/{endpoint}"
            while True:
                async with session.get(
                    url,
                    headers={"Authorization": f"Bearer {token}"},
                    params=params,
                ) as response:
                    if response.status != 200:
                        self.stdout.write(self.style.ERROR(f"Failed to fetch data for endpoint {endpoint}. Status: {response.status}"))
                        break
                    data = await response.json()
                results = data.get("results", [])
                if not results:
                    break
                for record in results:
                    await sync_to_async(self.save_record)(endpoint, record)
                paging = data.get("paging", {})
                next_page = paging.get("next", {}).get("after")
                if next_page:
                    params["after"] = next_page
                else:
                    break
            await sync_to_async(self.update_last_sync)(endpoint)

    def get_last_sync(self, endpoint):
        from hubspot_sync.models import HubSpotSyncHistory
        try:
            history = HubSpotSyncHistory.objects.get(endpoint=endpoint)
            return history.last_synced_at
        except HubSpotSyncHistory.DoesNotExist:
            return None

    def update_last_sync(self, endpoint):
        from hubspot_sync.models import HubSpotSyncHistory
        history, _ = HubSpotSyncHistory.objects.get_or_create(endpoint=endpoint)
        history.last_synced_at = timezone.now()
        history.save()

    def save_record(self, endpoint, record):
        if endpoint == "jobs":
            key = record.get("job_id")
            if key is None:
                return
            fields = extract_job_fields(record)
            Job.objects.update_or_create(job_id=key, defaults=fields)
        elif endpoint == "divisions":
            key = record.get("id")
            if key is None:
                return
            fields = extract_division_fields(record)
            Division.objects.update_or_create(id=key, defaults=fields)
        elif endpoint == "employees":
            key = record.get("hs_object_id")
            if key is None:
                return
            fields = extract_employee_fields(record)
            Employee.objects.update_or_create(hs_object_id=key, defaults=fields)
        else:
            self.stdout.write(self.style.WARNING(f"Endpoint {endpoint} not specifically handled; record skipped."))

def extract_job_fields(record):
    return {
        "job_id": record.get("job_id"),
        "add_date": record.get("add_date"),
        "add_user_id": record.get("add_user_id"),
        "cancel_date": record.get("cancel_date"),
        "contract_amount": record.get("contract_amount"),
        "job_value": record.get("job_value"),
        "hs_object_id": record.get("hs_object_id"),
        "hubspot_createdate": record.get("hs_createdate"),
        "hubspot_lastmodifieddate": record.get("hs_lastmodifieddate"),
    }

def extract_division_fields(record):
    return {
        "id": record.get("id"),
        "abbreviation": record.get("abbreviation"),
        "group_id": record.get("group_id"),
        "is_corp": record.get("is_corp"),
        "is_inactive": record.get("is_inactive"),
        "hs_object_id": record.get("hs_object_id"),
        "hubspot_createdate": record.get("hs_createdate"),
        "hubspot_lastmodifieddate": record.get("hs_lastmodifieddate"),
    }

def extract_employee_fields(record):
    return {
        "firstname": record.get("firstname"),
        "lastname": record.get("lastname"),
        "email": record.get("email"),
        "employee_division_id": record.get("employee_division_id"),
        "employee_title_id": record.get("employee_title_id"),
        "hs_object_id": record.get("hs_object_id"),
        "hubspot_createdate": record.get("hs_createdate"),
        "hubspot_lastmodifieddate": record.get("hs_lastmodifieddate"),
    }
