# hubspot

This project is a Django application that connects to the HubSpot API, downloads data from multiple endpoints, and stores the data in a local PostgreSQL database. It is containerized using Docker and managed with Docker Compose.

## Features

- **Endpoint Discovery:** Automatically discover available endpoints via the HubSpot CRM schemas endpoint if none are specified.
- **Separate Models:** Uses separate Django models (e.g., `Job`, `Division`, `Employee`) to store data from each HubSpot endpoint.
- **Incremental Sync:** Downloads only updated records on subsequent runs using a "last run" timestamp.
- **Asynchronous Processing:** Uses asynchronous API calls (with `aiohttp` and `asyncio`) to process multiple endpoints concurrently.
- **Dockerized Setup:** Easily deploy the application and PostgreSQL database using Docker and Docker Compose.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Environment Variables

The system requires several environment variables. You can set these in your environment or create a `.env` file in the project root. The required variables include:

- `HUBSPOT_API_TOKEN` – Your HubSpot API token (from your private app).
- `DATABASE_NAME` – The PostgreSQL database name (default: `postgres`).
- `DATABASE_USER` – The PostgreSQL username (default: `postgres`).
- `DATABASE_PASSWORD` – The PostgreSQL password.
- `DATABASE_HOST` – The database host (inside Docker Compose, this should be `db`).
- `DATABASE_PORT` – The PostgreSQL port (default: `5432`).
- `CONCURRENT` – (Optional) Number of endpoints to process concurrently (default: `5`).

Example `.env` file:

```env
HUBSPOT_API_TOKEN=your_hubspot_api_token_here
DATABASE_NAME=your_database_name
DATABASE_USER=your_database_user
DATABASE_PASSWORD=your_database_password
DATABASE_HOST=db
DATABASE_PORT=5432
CONCURRENT=5
