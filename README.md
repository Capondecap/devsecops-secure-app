<<<<<<< HEAD
# devsecops-secure-app
=======
# devsecops-secure-app

## Project Overview

`devsecops-secure-app` is a small DevSecOps demonstration project built around a Python Flask application, containerized local infrastructure, and an automated security pipeline. The application intentionally includes three common web security weaknesses so the surrounding tooling can be used to detect, monitor, and review them in a controlled environment.

## Architecture

The project consists of three runtime services:

- A Flask application that serves HTTP traffic on port `5000`
- A Prometheus instance that scrapes application metrics from port `8000`
- A Grafana instance for visualizing monitoring data

For delivery automation, the repository also includes:

- A GitHub Actions workflow for application and container security checks
- A shell deployment script for local container build and startup

## Tech Stack

- Python 3.10
- Flask
- Prometheus Python client
- Docker and Docker Compose
- Prometheus
- Grafana
- GitHub Actions
- Bandit
- pip-audit
- Trivy
- SQLite

## DevSecOps Pipeline

The GitHub Actions workflow runs on every push and performs a minimal security gate for the repository.

Pipeline stages:

1. Check out the repository
2. Set up Python 3.10
3. Install application dependencies and security tools
4. Run `bandit -r app -ll` for static analysis
5. Run `pip-audit` against Python dependencies
6. Build the Docker image for the application
7. Install Trivy
8. Scan the Docker image for container vulnerabilities

The workflow is configured to fail when any of the security scanning steps detect issues.

## Monitoring

Monitoring is provided through Prometheus and Grafana.

- The Flask application exposes Prometheus metrics on port `8000`
- Prometheus scrapes the application metrics endpoint using the configuration in `monitoring/prometheus.yml`
- Grafana runs on port `3000` and can be connected to Prometheus as a data source for dashboarding

This setup provides a simple base for request-level observability and future operational metrics.

## Automation

The `scripts/deploy.sh` script provides a basic local deployment workflow.

It performs the following actions:

1. Builds the project containers
2. Starts the services in detached mode
3. Displays the currently running containers

This script is intended for local environment setup and quick stack validation.

## Vulnerabilities

The application currently contains three intentionally insecure patterns for security testing and training.

### Command Injection

The `/ping` route passes user-controlled input into an operating system command using `os.popen`.

### Insecure Deserialization

The `/load` route accepts Base64-encoded data and deserializes it using `pickle.loads`.

### SQL Injection

The `/users` route builds a SQLite query through string concatenation with user input.

## How to Run Locally

### Prerequisites

- Docker
- Docker Compose

### Start the stack

```bash
docker compose up --build
```

Or use the deployment script:

```bash
sh scripts/deploy.sh
```

### Service endpoints

- Application: `http://localhost:5000`
- Prometheus metrics: `http://localhost:8000`
- Prometheus UI: `http://localhost:9090`
- Grafana UI: `http://localhost:3000`

## Security Improvements

The current project is intentionally insecure by design. Typical hardening steps would include:

- Replace shell command execution with safe parameter handling or remove it entirely
- Eliminate unsafe deserialization and use validated structured formats such as JSON
- Use parameterized SQL queries instead of string concatenation
- Add authentication and authorization controls where needed
- Introduce dependency pinning and scheduled update review
- Add container hardening such as non-root execution and reduced image surface
- Expand monitoring with security-relevant application and infrastructure alerts

## Security Considerations

This project demonstrates both exploitation and mitigation of common vulnerabilities.

- Exploitation details: `docs/exploitation.md`
- Mitigation strategies: `docs/mitigation.md`

The project follows DevSecOps principles by integrating security testing, vulnerability analysis, and remediation practices into the development lifecycle.
>>>>>>> f55045a (Inital commit)
