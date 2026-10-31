# Cloud-Ready Task Manager – V1

A containerized task management web application built using Flask, PostgreSQL, Redis, Docker, Docker Compose, and GitHub Actions. This project demonstrates practical Cloud Engineering and DevOps concepts, including application containerization, database integration, caching, automated testing, and Continuous Integration.

**Project Status:** V1 Development Completed | Azure Deployment Pending

---

## 1. Project Overview

The Cloud-Ready Task Manager is a web-based application that allows users to manage their daily tasks.

The application is designed using a multi-container architecture. Flask handles application logic and API requests, PostgreSQL stores task information persistently, and Redis provides caching.

Docker and Docker Compose simplify application packaging and local deployment, while GitHub Actions automates testing and Docker image building.

The next milestone is deploying the application to Microsoft Azure.

## 2. Project Objectives

- Develop a task management application using Flask.
- Integrate PostgreSQL for persistent data storage.
- Integrate Redis for caching.
- Containerize the application using Docker.
- Manage multiple services using Docker Compose.
- Implement automated testing using pytest.
- Configure a CI pipeline using GitHub Actions.
- Prepare the application for cloud deployment on Microsoft Azure.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application programming language |
| Flask | Backend web framework |
| PostgreSQL | Relational database |
| Redis | Caching |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Git | Version control |
| GitHub | Source code repository |
| pytest | Automated testing |
| GitHub Actions | Continuous Integration |
| Azure Container Registry | Planned container image registry |
| Azure Container Apps | Planned application hosting |

## 4. System Architecture

### Current Local Architecture

```text
             User
               |
               v
        Flask Application
               |
        +------+------+
        |             |
        v             v
    PostgreSQL      Redis
    Database        Cache
```

Docker Compose manages the application, PostgreSQL, and Redis services.

### Planned Azure Architecture

```text
       Developer
           |
           v
         GitHub
           |
           v
     GitHub Actions
       CI Pipeline
           |
           v
   Azure Container Registry
           |
           v
   Azure Container Apps
           |
      Flask Application
           |
       +---+---+
       |       |
       v       v
   PostgreSQL Redis
```

*Note: The Azure architecture represents the planned deployment, not an already completed deployment.*

## 5. Application Features

The application is designed to support the following task management operations:

- Create new tasks.
- View existing tasks.
- Update task completion status.
- Delete tasks.
- Store task information in PostgreSQL.
- Use Redis for caching.
- Provide application health-check functionality.

### API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Load application interface |
| GET | `/health` | Application health check |
| GET | `/api/tasks` | Retrieve tasks |
| POST | `/api/tasks` | Create a task |
| PATCH | `/api/tasks/<id>` | Update task |
| DELETE | `/api/tasks/<id>` | Delete a task |

## 6. Docker Implementation

The application has been containerized using a Dockerfile.

Docker Compose is used to manage the application's supporting services.

The local environment includes:

- Flask application container.
- PostgreSQL database container.
- Redis cache container.
- Docker-managed persistent volumes.

### Important Docker Commands

Build and start the application:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

Stop the services:

```bash
docker compose down
```

Validate the Compose configuration:

```bash
docker compose config --quiet
```

## 7. Database and Caching

### PostgreSQL

PostgreSQL is used as the primary database for storing task information.

The database schema is maintained in:

```text
db/schema.sql
```

The application uses environment variables for database configuration.

### Redis

Redis is integrated as the application's caching layer.

The project uses a cache key for retrieving task information and a configured cache expiration time of 30 seconds.

### Environment Configuration

Sensitive and environment-specific configuration is handled using environment variables.

The project includes:

- `.env` – Local environment configuration.
- `.env.example` – Example environment configuration.

**Security:** Never commit actual passwords, credentials, or secrets to GitHub.

## 8. Automated Testing

The project uses pytest for automated testing.

Test files are maintained in:

```text
tests/
```

The test file was named:

```text
tests/test_app.py
```

Run the test suite using:

```bash
python -m pytest -v
```

## 9. GitHub Actions – Continuous Integration

A GitHub Actions workflow has been configured at:

```text
.github/workflows/ci.yml
```

The workflow runs when code is pushed or a pull request is created.

### CI Pipeline Steps

1. Check out the repository.
2. Set up Python 3.11.
3. Install application dependencies and pytest.
4. Execute automated tests.
5. Build the Docker image.

The initial workflow failure caused by pytest not being installed on the GitHub Actions runner was fixed by adding pytest installation to the workflow.

The updated workflow was validated, reviewed, and merged into the main branch.

**Result:** The GitHub Actions CI workflow completed successfully.

## 10. Project Structure

The project directory is organized approximately as follows:

```text
Cloud_Task_Manager/
│
├── app/
│   ├── app.py
│   ├── requirements.txt
│   ├── static/
│   └── templates/
│
├── db/
│   └── schema.sql
│
├── tests/
│   └── test_app.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── Dockerfile
├── compose.yml
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## 11. Current Project Progress

| Component | Status |
|---|---|
| Flask application | Implemented |
| PostgreSQL integration | Implemented |
| Redis integration | Implemented |
| Dockerfile | Implemented |
| Docker Compose | Implemented |
| Local container startup | Verified by project testing |
| GitHub repository | Configured |
| pytest integration | Implemented |
| GitHub Actions CI | Successfully executed |
| Azure Container Registry | Pending |
| Azure Container Apps | Pending |
| Cloud PostgreSQL connectivity | Pending |
| Cloud Redis connectivity | Pending |
| Public application deployment | Pending |
| Live application verification | Pending |

## 12. Future Work – Azure Deployment

The next phase is to deploy Version 1 to Microsoft Azure.

Planned activities:

1. Verify Azure subscription and available credits.
2. Review estimated Azure resource costs.
3. Create Azure Container Registry.
4. Build and push the Docker image to ACR.
5. Deploy the application using Azure Container Apps.
6. Configure cloud database connectivity.
7. Configure Redis connectivity.
8. Configure environment variables and secrets.
9. Enable public HTTPS ingress.
10. Verify all application operations through the live URL.
11. Inspect application logs and health status.
12. Document the final deployment architecture.

Azure resources will be created only after checking the available subscription and estimated costs.

## 13. Learning Outcomes

Through this project, the following practical concepts have been covered:

- Flask application development.
- REST API implementation.
- PostgreSQL database integration.
- Redis caching.
- Docker image creation.
- Multi-container application management.
- Docker Compose configuration.
- Environment variable management.
- Git and GitHub workflows.
- Automated testing using pytest.
- GitHub Actions CI pipeline.
- Troubleshooting containerized applications.

The upcoming Azure deployment phase will provide practical experience with cloud infrastructure, container registries, managed application hosting, and cloud service connectivity.

## 14. Repository

**GitHub Repository:**  
https://github.com/Kiran-Abrams/Cloud-task-Manager

---

**Project:** Cloud-Ready Task Manager  
**Version:** 1.0  
**Category:** Cloud Engineering / DevOps  
**Development Status:** Completed  
**Deployment Status:** Azure deployment pending

Built as a hands-on Cloud Engineering and DevOps learning project.