# Database Connectivity Course Lab (Step-by-Step)

## Objective
Build hands-on database connectivity skills by running small, verifiable CRUD steps for multiple database types using Python and Docker.

## Learning Outcomes
After completing this repository, students can:
- configure database connection settings without hardcoding credentials
- connect to relational, document, key-value, graph, wide-column, and search databases
- run CRUD as a clear step-by-step process
- verify final state after deletion

## Prerequisites
- Docker + Docker Compose
- Python 3.10+
- pip

## Repository Map
```text
.
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── config/
│   ├── postgresql.properties
│   ├── mongodb.properties
│   ├── redis.properties
│   ├── neo4j.properties
│   ├── cassandra.properties
│   └── elasticsearch.properties
├── labs/
│   ├── common/config_loader.py
│   ├── postgresql/
│   ├── mongodb/
│   ├── redis/
│   ├── neo4j/
│   ├── cassandra/
│   └── elasticsearch/
└── docs/student_checklist.md
```

## Setup
1. Clone and enter repository.
2. Create virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

## Configuration (.env + properties)
1. Create a local env file:
   ```bash
   cp .env.example .env
   ```
2. Review `config/*.properties` files and set lab-safe values.
3. Scripts load values in this order:
   - environment variable (highest priority)
   - `config/<db>.properties` value
4. Never hardcode credentials in scripts.

## Start database containers
```bash
docker compose up -d
docker compose ps
```

Health/wait notes:
- Start all containers first, then wait before running labs.
- Cassandra and Elasticsearch may need 30-90 seconds to become ready.
- If Step 1 fails, wait and retry `01_connect.py`.

## Run each mini-lab
Run from repository root:

### PostgreSQL (Relational)
- Guide: `labs/postgresql/README.md`
- Steps: `python labs/postgresql/01_connect.py` ... `python labs/postgresql/06_verify.py`

### MongoDB (Document)
- Guide: `labs/mongodb/README.md`
- Steps: `python labs/mongodb/01_connect.py` ... `python labs/mongodb/06_verify.py`

### Redis (Key-Value)
- Guide: `labs/redis/README.md`
- Steps: `python labs/redis/01_connect.py` ... `python labs/redis/06_verify.py`

### Neo4j (Graph)
- Guide: `labs/neo4j/README.md`
- Steps: `python labs/neo4j/01_connect.py` ... `python labs/neo4j/06_verify.py`

### Cassandra (Wide-Column)
- Guide: `labs/cassandra/README.md`
- Steps: `python labs/cassandra/01_connect.py` ... `python labs/cassandra/06_verify.py`

### Elasticsearch (Search)
- Guide: `labs/elasticsearch/README.md`
- Steps: `python labs/elasticsearch/01_connect.py` ... `python labs/elasticsearch/06_verify.py`

## Troubleshooting
- **Module not found**: ensure venv is active and `pip install -r requirements.txt` completed.
- **Config error**: fill missing keys in `.env` or matching `config/<db>.properties`.
- **Connection refused/timeouts**: check `docker compose ps`, ports, and retry after wait.
- **Auth failed**: confirm credentials in `.env` match container environment values.

## Submission / Evidence Checklist
Use `docs/student_checklist.md` to capture evidence for all CRUD stages and reflection questions.

## Stop the lab
```bash
docker compose down
```
Remove volumes if needed:
```bash
docker compose down -v
```
