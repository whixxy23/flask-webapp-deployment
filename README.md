# Docker & Containerization — Module 4

Containerized a Flask web application using Docker and Docker Compose, with PostgreSQL running as a separate container.

**Flow:** Application Code → Dockerfile → Image → Container → Docker Compose → Running Application

---

## What I Built

* Created a Dockerfile for the Flask application.
* Built a custom Docker image for the web application.
* Ran the Flask app inside a Docker container.
* Added PostgreSQL as a separate container.
* Connected the application and database through a Docker Compose network.
* Used a named Docker volume to persist PostgreSQL data.
* Used environment variables for database configuration.
* Added `.dockerignore` to keep unnecessary files out of the image.

---

## Docker Architecture

```text
                    Docker Compose
                         │
          ┌──────────────┴──────────────┐
          │                             │
     Flask Web App                 PostgreSQL
      Container                    Container
          │                             │
          └──────── Docker Network ─────┘
                         │
                  PostgreSQL Volume
```

The Flask container communicates with PostgreSQL using the Compose service name `db` rather than `localhost`.

---

## Key Docker Concepts Practiced

### Images

Built a custom image from the application's `Dockerfile`.

### Containers

Ran the Flask application and PostgreSQL database as isolated containers.

### Networking

Docker Compose automatically created a network allowing the containers to communicate with each other.

### Volumes

A named volume was attached to PostgreSQL so database data survives container recreation.

### Environment Variables

Database configuration is supplied through environment variables rather than being hardcoded into the application.

---

## Useful Commands

```bash
# Build the image
docker compose build

# Start the containers
docker compose up -d

# Check running containers
docker compose ps

# View logs
docker compose logs

# Stop the application
docker compose down

# Stop containers without removing the database volume
docker compose down

# Inspect volumes
docker volume ls
```

---

## Verification

The application was tested from the browser after starting the Compose stack.

Container status:

```bash
docker compose ps
```

Application logs:

```bash
docker compose logs web
```

Database logs:

```bash
docker compose logs db
```

The PostgreSQL data is stored in a Docker named volume rather than inside the application container.

---

## Project Structure

```text
.
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .env.example
├── .gitignore
└── README.md
```

> `.env` contains local database credentials and is excluded from Git.

---

## Key Learnings

* Containers package applications and their dependencies into reproducible environments.
* Docker Compose makes running multi-container applications much simpler.
* Containers can communicate through Docker's internal networking.
* Persistent application data should not depend on a container's writable filesystem.
* Environment variables provide a cleaner way to configure containers without hardcoding secrets.

### Module 4 Outcome

The Flask application that was previously deployed directly on AWS EC2 in Module 3 was successfully packaged and run as a containerized application with PostgreSQL using Docker Compose.
