import asyncio
from datetime import datetime

import aiohttp
from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from hubspot_sync.models import HubSpotData, HubSpotSyncHistory, Job, Division, Employee


class Command(BaseCommand):
    help = "Sync data from HubSpot API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--endpoint",
            nargs="+",
            help="Specify one or more endpoints to sync. If omitted, all available endpoints will be discovered.",
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
            tasks = [
                self.sync_endpoint(ep, token, session, semaphore)
                for ep in endpoints
            ]
            await asyncio.gather(*tasks)

    async def discover_endpoints(self, session, token):
        url = "https://api.hubapi.com/crm/v3/schemas"
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                self.stdout.write(
                    self.style.ERROR(f"Failed to discover endpoints. Status: {response.status}")
                )
                return []
            data = await response.json()
        endpoints = [
            schema.get("objectTypeId")
            for schema in data.get("results", [])
            if schema.get("objectTypeId")
        ]
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
                        self.stdout.write(
                            self.style.ERROR(
                                f"Failed to fetch data for endpoint {endpoint}. Status: {response.status}"
                            )
                        )
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
        try:
            history = HubSpotSyncHistory.objects.get(endpoint=endpoint)
            return history.last_synced_at
        except HubSpotSyncHistory.DoesNotExist:
            return None

    def update_last_sync(self, endpoint):
        history, _ = HubSpotSyncHistory.objects.get_or_create(endpoint=endpoint)
        history.last_synced_at = timezone.now()
        history.save()

    def save_record(self, endpoint, record):
        # For the "jobs" endpoint (or its known aliases)
        print("endpoint received:", endpoint)
        print("Record received:", record)
        

        if endpoint.lower() in ['jobs', 'p47947320_jobs', '2-37778614']:
            job_data = {}
            job_field_names = {field.name for field in Job._meta.get_fields() if field.concrete and not field.auto_created}
            print("job_field_names:", job_field_names)
            for key in job_field_names:
                if key in record:
                    job_data[key] = record[key]
                    print("Job (", key, "): ", record[key])
            #Job.objects.update_or_create(job_id=job_data.get("job_id"), defaults=job_data)

        # # For the "divisions" endpoint (or its known aliases)
        elif endpoint.lower() in ['divisions', 'p47947320_divisions', '2-37778609']:
            division_data = {}
            division_field_names = {field.name for field in Division._meta.get_fields() if field.concrete and not field.auto_created}
            for key in division_field_names:
                if key in record:
                    division_data[key] = record[key]
                    print("division_data (", key, "): ", record[key])
        #     Division.objects.update_or_create(id=division_data.get("id"), defaults=division_data)

        # # For the "employees" endpoint (or its known aliases)
        elif endpoint.lower() in ['employees', 'p47947320_employees', '2-38071071']:
            employee_data = {}
            employee_field_names = {field.name for field in Employee._meta.get_fields() if field.concrete and not field.auto_created}
            for key in employee_field_names:
                if key in record:
                    employee_data[key] = record[key]
                    print("employee_data (", key, "): ", record[key])
        #     # Use the unique HubSpot record id ("hs_object_id") if available.
        #     Employee.objects.update_or_create(hs_object_id=employee_data.get("hs_object_id"), defaults=employee_data)

        # # Fallback: store the record in the generic table.
        # else:
        #     record_id = record.get("id") or record.get("job_id")
        #     HubSpotData.objects.update_or_create(
        #         endpoint=endpoint,
        #         record_id=record_id,
        #         defaults={"data": record},
        #     )
