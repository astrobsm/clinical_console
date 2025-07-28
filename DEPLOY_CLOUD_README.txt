# Cloud/Server Deployment Guide

## 1. Prerequisites
- Docker and docker-compose installed on your server (Linux, Windows, or cloud VM)
- Domain name (optional, for HTTPS)

## 2. Environment Variables
- Edit `backend/.env` and `frontend/.env` with production values (secrets, API URLs, DB config)

## 3. Build & Deploy
- From project root, run:
  docker-compose up --build -d
- This will build and start both backend (Flask) and frontend (React/Nginx) containers

## 4. Expose Ports
- Ensure ports 80 (frontend) and 5000 (backend, if needed) are open in your firewall/security group
- For HTTPS, use a reverse proxy (see below)

## 5. HTTPS (Recommended)
- Use Nginx or Caddy as a reverse proxy for SSL termination
- Example (Nginx):
  - Install certbot and nginx
  - Point your domain to the server IP
  - Use certbot to generate SSL certs
  - Proxy / to frontend:80 and /api to backend:5000

## 6. Update & Rollback
- To update: pull new code, re-run `docker-compose up --build -d`
- To stop: `docker-compose down`

## 7. Troubleshooting
- Check logs: `docker-compose logs -f`
- Check container status: `docker ps`

---
Automated by GitHub Copilot.
