
# ToDoList Application

Simple full-stack ToDo list application with a FastAPI backend and a static frontend served via Nginx. The project includes Docker Compose setup for local development, database dump/restore scripts, and a small set of helper scripts to get started quickly.

## Contents
- **Project:** Lightweight ToDo list API and frontend
- **Backend:** FastAPI (async) running with Uvicorn
- **Database:** PostgreSQL (containerized)
- **Frontend:** Static files served by Nginx

## Prerequisites
- Docker and Docker Compose installed on your machine
- Make sure ports 80 are available (or adjust `docker-compose.yml`)

## Quick Start (Local Development)

1. Make helper scripts executable if needed:
   ```bash
   chmod +x setup.sh
   ```

2. Run the setup script to prepare the environment (creates .env, data folders, etc.):
   ```bash
   ./setup.sh
   ```

3. Start services with Docker Compose: (no need for first time after using `./setup.sh`)
   ```bash
   sudo docker compose up --build
   ```

This will start three services defined in `docker-compose.yml`: `db`, `backend`, and `frontend`.

## Environment Variables
The project expects a `.env` file with the following variables (an example may be created by `setup.sh`):

- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

The backend service reads `DATABASE_URL` from the environment (set automatically in `docker-compose.yml` when using `.env`).

## Database Dump and Restore

- To create a dump of the database (Postgres dump included in repo):
  ```bash
  ./dump_database.sh
  ```

- To restore the database from `todo_db.dump`:
  ```bash
  ./restore_database.sh
  ```

## Health Check
Run the included health check script to verify services are reachable:
```bash
./check_health.sh; echo exit_code:$?
```

## Backend Notes
- Backend code is in the `backend-api/` folder.
- Start locally (inside container via compose) uses:
  ```bash
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload
  ```
- API routes are under `backend-api/api/api_v1/endpoints/` (users, tasks, categories).

## Development
- To edit backend code during development, the backend service mounts `./backend-api` into the container, so code changes reload automatically when using the Uvicorn `--reload` flag.

## Project Structure (Top-level)
- `backend-api/` — FastAPI app, database models, schemas, and CRUD logic
- `frontend/` — Nginx config and static frontend files
- `db_data/` — Postgres persistent data (mounted as a Docker volume)
- `todo_db.dump` — Database dump (created after using `dump_database.sh`) (used by `restore_database.sh`)
- `setup.sh`, `dump_database.sh`, `restore_database.sh`, `check_health.sh` — helper scripts
