# Frontend & Backend Deployment Checklist

## 1. Production Build
- Run `npm run build` in `frontend/` (already done, see `build/` folder).
- All static assets (images, etc.) are included in the build output.

## 2. Environment Variables
- Frontend: Set `REACT_APP_API_URL` in `frontend/.env` to your backend API endpoint.
- Backend: Set all secrets and DB config in `backend/.env`.

## 3. Docker & Compose
- `frontend/Dockerfile` builds and serves the React app with Nginx.
- `backend/Dockerfile` builds the Flask API.
- `docker-compose.yml` orchestrates both services. Ports: 80 (frontend), 5000 (backend).

## 4. Deployment
- To deploy both services: `docker-compose up --build -d` from the project root.
- To update: re-run the above after code changes.

## 5. End-to-End Test
- After deployment, visit your frontend URL and log in with a test user to verify the full workflow.
- Check browser console and network tab for errors.

## 6. Notes
- For production, use secure secrets and HTTPS.
- Adjust CORS and API URLs as needed for your environment.
- For cloud or server deployment, point your domain to the server's IP and open ports 80/443.

---
Automated by GitHub Copilot.
