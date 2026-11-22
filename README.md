# OpsRescue
### Infrastructure Monitoring & Automated Incident Recovery System

**Detect failures. Execute recovery. Verify reliability.**

OpsRescue is a Python-based infrastructure monitoring and automated incident response system designed to monitor Linux host resources, detect service failures, execute automated recovery actions and maintain a persistent operational audit trail.

The platform combines Linux system monitoring, Docker container management, automated remediation and PostgreSQL-based incident tracking to demonstrate practical infrastructure reliability and Site Reliability Engineering (SRE) concepts.

---

## Overview

Modern infrastructure environments require continuous monitoring to maintain service availability and operational stability.

Unexpected service failures, resource exhaustion and container outages can interrupt application availability and require immediate investigation.

OpsRescue addresses these challenges through an automated monitoring and recovery workflow.

The system:

- Monitors CPU, memory and disk utilization.
- Tracks container and web-service availability.
- Detects infrastructure and application failures.
- Automatically attempts recovery of failed containers.
- Verifies service availability after recovery.
- Records incidents and recovery outcomes in PostgreSQL.
- Generates operational health and incident reports.

---

## Architecture

```text
             LINUX HOST ENVIRONMENT
                       |
                       v
              PYTHON MONITORING
                       |
             +---------+---------+
             |         |         |
             v         v         v
            CPU      MEMORY     DISK
             |         |         |
             +---------+---------+
                       |
                       v
                DOCKER ENGINE
                       |
             +---------+---------+
             |                   |
             v                   v
        NGINX SERVICE         POSTGRESQL
             |
             v
         HEALTH CHECK
             |
       +-----+------+
       |            |
       v            v
    HEALTHY       FAILED
                    |
                    v
             INCIDENT DETECTION
                    |
                    v
             AUTOMATED RECOVERY
                    |
                    v
             RECOVERY VERIFICATION
                    |
             +------+------+
             |             |
             v             v
          SUCCESS        FAILURE
             |             |
             v             v
          RESOLVED      ESCALATED
             |             |
             +------+------+
                    |
                    v
             POSTGRESQL AUDIT
                    |
                    v
             OPERATIONAL REPORTS
```

---

## Key Features

### 1. Linux Infrastructure Monitoring

Collects system-level resource information using Python and the `psutil` library.

Monitored parameters include:

- CPU utilization.
- Memory utilization.
- Disk utilization.
- Network data sent and received.
- System load averages.
- System uptime.
- Running process count.

### 2. Container Health Monitoring

Monitors the status of the containerized web service and checks its HTTP availability.

The system identifies service failures when the container stops or the web service becomes unresponsive.

### 3. Automated Incident Detection

Detects operational failures and identifies affected services.

When a monitored service becomes unavailable, the monitoring workflow initiates incident handling and recovery procedures.

### 4. Automated Service Recovery

Implements an automated remediation mechanism that attempts to restart failed containers.

The recovery workflow follows:

```text
Detect Service Failure
        |
        v
Identify Failed Container
        |
        v
Attempt Container Restart
        |
        v
Verify Service Availability
        |
    +---+---+
    |       |
    v       v
  Success  Failure
    |       |
    v       v
 Resolve  Escalate
 Incident  Incident
```

The system verifies recovery rather than assuming that restarting a container automatically resolves the problem.

### 5. PostgreSQL Incident Management

Maintains a persistent record of operational incidents using PostgreSQL.

Incident information includes:

- Incident timestamp.
- Severity.
- Affected service.
- Recovery action.
- Remediation outcome.

This provides an audit trail for investigating service disruptions and reviewing previous recovery attempts.

### 6. Operational Health Reporting

Generates reports containing:

- Current infrastructure status.
- Resource utilization.
- Incident history.
- Automated recovery outcomes.
- Recovery success information.

These reports help engineers understand infrastructure health and identify recurring operational problems.

### 7. Security-Conscious Configuration

Uses environment variables to manage database credentials.

The project also demonstrates:

- Excluding sensitive configuration files from version control.
- Parameterized SQL queries.
- Persistent database storage.
- Separation of monitoring and database logic.

---

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Operating System | Ubuntu Linux |
| System Monitoring | psutil |
| Containerization | Docker |
| Container Orchestration | Docker Compose |
| Web Server | NGINX |
| Database | PostgreSQL |
| Database Connectivity | psycopg2 |
| Configuration Management | python-dotenv |
| Automation | Python Scripting |
| Version Control | Git, GitHub |

---

## Project Structure

```text
OpsRescue/
│
├── logs/
│
├── monitor/
│   ├── monitor.py
│   ├── checks.py
│   ├── remediation.py
│   ├── database.py
│   └── report.py
│
├── .gitignore
├── docker-compose.yml
├── requirements.txt
├── architecture.png
└── README.md
```

### Component Responsibilities

| Component | Description |
|---|---|
| `monitor.py` | Main monitoring and incident-handling workflow |
| `checks.py` | Host resource and service health checks |
| `remediation.py` | Automated container restart and recovery verification |
| `database.py` | PostgreSQL connection and incident persistence |
| `report.py` | Operational report generation |
| `docker-compose.yml` | Container orchestration |
| `requirements.txt` | Python dependencies |
| `logs/` | Generated operational logs and reports |

---

## Installation and Setup

### Prerequisites

- Ubuntu Linux or compatible Linux environment.
- Python 3.
- Docker.
- Docker Compose.
- Git.

### Step 1: Clone the Repository

```bash
git clone https://github.com/onkarshirke/OpsRescue-Infrastructure-Monitoring-Recovery.git

cd OpsRescue-Infrastructure-Monitoring-Recovery
```

### Step 2: Configure Environment Variables

Create a `.env` file in the project root.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=infrawatch
DB_USER=infrawatch
DB_PASSWORD=your_password_here
```

Use your own database credentials. Keep `.env` excluded from Git.

### Step 3: Start Docker Containers

```bash
docker compose up -d
```

Verify running containers:

```bash
docker ps
```

### Step 4: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 5: Start Monitoring

```bash
cd monitor

python3 monitor.py
```

### Step 6: Generate an Operational Report

```bash
python3 report.py
```

---

## Failure Simulation and Recovery Demonstration

One of the central capabilities of OpsRescue is automated service recovery.

### Step 1: Start the Infrastructure

```bash
docker compose up -d
```

### Step 2: Simulate a Service Failure

Stop the monitored web container:

```bash
docker stop infrawatch-web
```

### Step 3: Run the Monitoring System

```bash
python3 monitor.py
```

### Step 4: Observe the Recovery Workflow

The monitoring system detects the service failure, attempts to restart the container and verifies its availability.

Example expected workflow:

```text
[DETECTION]
Service infrawatch-web is DOWN.

[REMEDIATION]
Attempting automatic container restart.

[VERIFICATION]
Checking service availability.

[RECOVERY]
Service recovery verified.

[INCIDENT]
Recovery outcome recorded in PostgreSQL.
```

Actual output depends on the runtime environment and recovery result.

---

## SRE Concepts Demonstrated

| Concept | Implementation |
|---|---|
| Infrastructure Monitoring | CPU, memory and disk monitoring |
| Service Availability | Container and HTTP health checks |
| Incident Detection | Failed-service identification |
| Automated Remediation | Container restart |
| Recovery Verification | Post-restart health checks |
| Incident Management | Persistent incident records |
| Database Management | PostgreSQL |
| Operational Reporting | Health and recovery reports |
| Linux Administration | Linux resource and service monitoring |
| Containerization | Docker and Docker Compose |

---

## Practical Use Cases

### Scenario 1: Web Service Failure

A monitored web service becomes unavailable.

OpsRescue detects the failure, attempts to restart the affected container and verifies whether the service has recovered.

### Scenario 2: High Resource Utilization

The Linux host experiences increased CPU, memory or disk utilization.

The monitoring system collects resource information to help identify potential infrastructure issues.

### Scenario 3: Repeated Service Failures

A service repeatedly becomes unavailable.

The incident history helps engineers investigate previous failures and review recovery outcomes.

### Scenario 4: Incident Investigation

An engineer needs to understand when a service failed and what recovery action was performed.

PostgreSQL incident records and operational reports provide information for investigation.

---

## Learning Outcomes

This project demonstrates practical understanding of:

- Linux system administration.
- Python infrastructure automation.
- Docker container management.
- Infrastructure health monitoring.
- Automated service recovery.
- PostgreSQL database integration.
- Incident tracking and reporting.
- Failure detection and recovery verification.
- Security-conscious configuration management.

---

## Future Enhancements

Potential improvements include:

- Prometheus metrics integration.
- Grafana monitoring dashboards.
- Email and messaging-based notifications.
- Multi-server infrastructure monitoring.
- Advanced incident severity classification.
- Service-level objective (SLO) tracking.
- Cloud infrastructure integration.
- Historical infrastructure performance analytics.

---

## Author

**Onkar Shirke**

GitHub: https://github.com/onkarshirke  
LinkedIn: https://linkedin.com/in/onkar-shirke

---

## Attribution

This project is based on the original InfraWatch implementation by Emmanuel Magala.

Original repository:  
https://github.com/EmmanuelMagala/infrawatch-monitoring

Preserve the original author's attribution and license when redistributing or modifying the implementation.

---

**OpsRescue – Building resilient infrastructure through monitoring and automated recovery.**
