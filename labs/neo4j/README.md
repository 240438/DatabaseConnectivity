# Neo4j Mini-Lab (Step-by-Step CRUD)

## Step 0 - Before you begin
1. From repository root, ensure containers are running: `docker compose up -d`.
2. Activate your Python virtual environment and install dependencies from root `requirements.txt`.
3. Confirm `.env` and `config/neo4j.properties` are filled with lab values.

## Step 1 - Connectivity check
Run:
```bash
python labs/neo4j/01_connect.py
```
Expected: success message (`✅ Connected ...`).

## Step 2 - Create
Run:
```bash
python labs/neo4j/02_create.py
```
Expected: one deterministic student record is created (`id` or key `1001` / `student-1001`).

## Step 3 - Read
Run:
```bash
python labs/neo4j/03_read.py
```
Expected: the inserted student values are printed (`Asha`, `DB Basics`).

## Step 4 - Update
Run:
```bash
python labs/neo4j/04_update.py
```
Expected: `before` shows original course and `after` shows `Advanced Databases`.

## Step 5 - Delete
Run:
```bash
python labs/neo4j/05_delete.py
```
Expected: the target student record is deleted.

## Step 6 - Verify final state
Run:
```bash
python labs/neo4j/06_verify.py
```
Expected: verify step confirms the record is absent.

## Common mistakes and fixes
- **Config missing**: fill `.env` and `config/neo4j.properties`; scripts print missing keys.
- **Container not ready**: wait 20-60 seconds (Cassandra/Elasticsearch often need more time) and retry Step 1.
- **Wrong port/host**: compare your config with `docker compose ps`.

## Checkpoint questions
1. Which connection values came from environment variables?
2. What deterministic ID/key did this lab use?
3. Which step proves deletion happened successfully?
