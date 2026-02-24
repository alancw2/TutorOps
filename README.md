# TutorOps

TutorOps is a lightweight full-stack tutoring operations platform for managing clients, session logs, and earnings analytics. It provides a FastAPI backend with a SQLite database and a minimal JavaScript dashboard for real-time interaction.

---

## Features

- RESTful API for clients and session management  
- SQLite persistence using SQLModel ORM  
- Aggregate analytics for hours and revenue  
- Minimal vanilla JS dashboard  
- Fully containerized with Docker Compose  
- Automated pytest test suite  

---

## Tech Stack

**Backend**
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Pytest

**Frontend**
- Vanilla JavaScript
- HTML/CSS
- Nginx (static serving via Docker)

**DevOps**
- Docker
- Docker Compose

---

## Project Structure
TutorOps/
├── backend/
│ ├── app/
│ │ ├── routers/
│ │ ├── models.py
│ │ ├── schemas.py
│ │ ├── db.py
│ │ └── main.py
│ ├── tests/
│ └── Dockerfile
├── frontend/
│ ├── index.html
│ ├── app.js
│ └── styles.css
└── docker-compose.yml

---

## Quick Start (Recommended)

Run the full stack with Docker:

```bash

docker compose up --build

Then open:

-Frontend dashboard: http://localhost:5173

-API docs: http://localhost:8000/docs

-Health check: http://localhost:8000/health

## API Overview
Clients

POST /clients/ — create client

GET /clients/ — list clients

GET /clients/{client_id} — get client

GET /clients/{client_id}/sessions — sessions for client

GET /clients/{client_id}/summary — client analytics

Sessions

POST /sessions/ — create session

GET /sessions/ — list sessions

GET /sessions/{session_id} — get session

Analytics

GET /summary — global platform metrics

## Running Backend Only (Local Dev)
** From backend/: **
uvicorn app.main:app --reload
** API will be available at: **
http://localhost:8000

## Testing
** Run the automated test suite **
pytest -q

## Design Notes
- Uses dependency injection for database sessions

- Relational modeling between Client and Session

- Designed for portability with SQLite

- Containerized for reproducible local deployment

- Minimal frontend intentionally avoids heavy frameworks

## Further Improvements
- Uses dependency injection for database sessions

- Relational modeling between Client and Session

- Designed for portability with SQLite

- Containerized for reproducible local deployment

- Minimal frontend intentionally avoids heavy frameworks

## Author
** Alan Ward **
UIUC Mathematics 
Github: https://github.com/alancw2
