# BPRS UNTH EMR Backend

This is a Flask REST API backend for the Burns, Plastic, and Reconstructive Surgery (BPRS) unit EMR system at UNTH.

## Features
- User authentication (JWT) and role-based access (consultant, senior registrar, registrar, house officer, admin)
- Patient registration and management
- Clinical evaluation, diagnosis, treatment plan, investigations, wound care, surgery booking, appointments
- Notifications, academic events, assessments, CBT questions, and scoring
- PostgreSQL database
- Environment variable configuration
- Ready for Dockerization

## Setup
1. Copy `.env.example` to `.env` and fill in your secrets and database URL.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run database migrations:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
4. Start the server:
   ```bash
   flask run
   ```

## API Endpoints
- To be documented in future updates.
