# Deployment

## Backend
Set the existing LLM and PostgreSQL environment variables from `.env.example`, plus:

`CORS_ORIGINS=https://YOUR-FRONTEND-DOMAIN`

Start command:

`uvicorn api.server:app --host 0.0.0.0 --port $PORT`

## Frontend
Set `VITE_API_URL` to the deployed backend `/api` URL.

Build:

`cd frontend && npm install && npm run build`

Deploy the `frontend/dist` folder to Vercel, Netlify, or another static host.

## Important security note
The existing ETL transform tool executes LLM-generated Python with `exec()`. Do not expose arbitrary transform execution publicly until it is isolated in a sandbox/container with strict resource and filesystem limits. The extraction endpoint is intended as the first safe web workflow.
