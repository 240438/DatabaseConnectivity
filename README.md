# Database Connectivity Lab (Python + Docker)

This ready-to-run lab teaches students how applications connect to databases and how to safely provide connection settings externally.

## Learning Objectives

By the end of this lab, students will be able to:
1. Explain why apps need a database endpoint, username, and password.
2. Use database libraries in Python for different database categories.
3. Avoid hardcoding endpoint/username/password in source code.
4. Provide configuration through:
   - Environment variables
   - External configuration/properties file
5. Implement CRUD operations for multiple database types.

## Database Types Covered

- **Key-Value**: Redis
- **Wide-Column**: Cassandra
- **Document**: MongoDB
- **Relational**: PostgreSQL
- **Graph**: Neo4j
- **Search**: Elasticsearch

## Repository Structure

```text
.
├── docker-compose.yml
└── python_lab
    ├── config.example.ini
    ├── config_loader.py
    ├── requirements.txt
    ├── redis_crud.py
    ├── cassandra_crud.py
    ├── mongodb_crud.py
    ├── postgres_crud.py
    ├── neo4j_crud.py
    └── elasticsearch_crud.py
```

## Part 1 - Start Databases in Docker

From repository root:

```bash
docker compose up -d
```

Check containers:

```bash
docker compose ps
```

## Part 2 - Python Setup

```bash
cd python_lab
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Part 3 - External Configuration (No Hardcoding)

### 3.1 Create properties/config file

```bash
cp config.example.ini config.ini
```

`config_loader.py` reads from `config.ini` (or file path from `APP_CONFIG_FILE`).

### 3.2 Override with environment variables

Students can override any value externally, for example:

```bash
export POSTGRES_HOST=localhost
export POSTGRES_PORT=5432
export POSTGRES_USERNAME=appuser
export POSTGRES_SECRET=apppass
export POSTGRES_DATABASE=appdb
```

> This demonstrates best practice: **credentials and endpoints are external**, not hardcoded in code.
> In this lab template, the config key name `secret` stores the database password value.

## Part 4 - Run CRUD Labs (One-by-One)

From `python_lab` directory:

```bash
python redis_crud.py
python cassandra_crud.py
python mongodb_crud.py
python postgres_crud.py
python neo4j_crud.py
python elasticsearch_crud.py
```

Each script demonstrates:
- **Create** record/document/node/value
- **Read** it
- **Update** it
- **Delete** it

## Part 5 - Student Practical Tasks

### Task A: Connectivity Concepts
1. Identify endpoint, username, and password value (`secret` key) for each database in `config.ini`.
2. Explain where each value is used in Python code.
3. Prove no connection values are hardcoded in the CRUD logic.

### Task B: Environment Variable Override
1. Run one script using only `config.ini`.
2. Override one setting using environment variables (example: `POSTGRES_HOST`).
3. Re-run and document the observed behavior.

### Task C: CRUD Validation for All Database Types
For each of the 6 databases:
1. Run script.
2. Capture output of CREATE, READ, UPDATE, DELETE.
3. Submit evidence (terminal output screenshot or text log).

### Task D: Extend the Lab
1. Add one more field (`email`) for student entity in all scripts.
2. Update CREATE/READ/UPDATE/DELETE accordingly.
3. Demonstrate successful execution after change.

### Task E: Reflection Questions
1. Why is hardcoding endpoint/username/password risky?
2. What is the difference between using env vars and properties files?
3. Which database type best fits:
   - Session store
   - Social graph
   - Product catalog
   - Full-text search
4. What operational challenges did you observe with running many database engines together?

## Instructor Notes

- Cassandra may take longer than other services to become ready.
- Elasticsearch and Neo4j use more memory than Redis/PostgreSQL.
- If a script fails due to service readiness, wait and rerun.

## Stop Lab

From repository root:

```bash
docker compose down
```

To remove volumes too:

```bash
docker compose down -v
```
