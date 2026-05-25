# Spring Boot 2.7 + Vue 3 Project

This template separates a Spring Boot 2.7 backend and a Vue 3 + Vite frontend.

## Project Structure

```text
.
|-- backend/           # Spring Boot API
|-- frontend/          # Vue 3 + Vite
|-- .devcontainer/     # Dev Container config
`-- docker-compose.yml # Dev container runtime
```

## Run With Docker

```bash
docker compose up -d --build backend frontend
```

Check logs:

```bash
docker compose logs -f backend frontend
```

Stop:

```bash
docker compose down
```

Endpoints:

- Backend: `http://localhost:8080/api/hello`
- Frontend: `http://localhost:5173`

## Run Dev Container Service (Optional)

`dev` service is assigned to a profile so it does not start by default.

```bash
docker compose --profile devcontainer up -d dev
docker compose exec dev bash
```

## Run Without Docker

Requirements:

- JDK 8+
- Maven 3.8+
- Node.js 18+
- npm 9+

Backend:

```bash
cd backend
mvn spring-boot:run
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

