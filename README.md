An internal backend service for CHISL, built with FastAPI, to sync time logs and metadata from Clockify into a PostgreSQL database. Designed for modularity, reliability, and extensibility.

Backend Stack
FastAPI for the backend web framework

Clockify API for time tracking data

PostgreSQL as the data store

Prefect for background sync jobs

SQLAlchemy for DB interaction


clockify_sync_chisl/
├── api_client/
│   └── clockify_client.py       # Clockify API logic
├── db/
│   └── postgres_handler.py      # PostgreSQL interaction logic
├── scheduler/
│   └── job_runner.py            # Optional scheduler (e.g., APScheduler)
├── schemas.py                   # Pydantic models for requests/responses
├── config.py                    # App settings & credentials
├── models.py                    # SQLAlchemy (ORM) or DB schema mappings
├── main.py                      # FastAPI app entry point
├── utils/
│   └── transform.py             # Raw-to-clean data transformer
└── README.md


uvicorn main:app --reload

Running the Backend
Start the FastAPI app (from the project root):

bash
Copy
Edit
uvicorn main:app --reload
Access the automatic interactive docs here:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

CLOCKIFY_API_KEY=your_api_key
POSTGRES_CONN=postgresql://user:pass@host:port/db



