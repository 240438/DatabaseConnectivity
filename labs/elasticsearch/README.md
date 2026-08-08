# Elasticsearch Mini-Lab (Step-by-Step CRUD)

## Step 0 - Before you begin
1. From repository root, ensure containers are running: `docker compose up -d`.
2. Activate your Python virtual environment and install dependencies from root `requirements.txt`.
3. Confirm `.env` and `config/elasticsearch.properties` are filled with lab values.

## Step 1 - Connectivity check
Run:
```bash
python labs/elasticsearch/01_connect.py
```
Expected: success message (`✅ Connected ...`).

## Step 2 - Create index (if needed)
Run:
```bash
python labs/elasticsearch/07_create_index.py
```
Purpose: creates the configured index (no-op if it already exists). This prepares the index before bulk ingesting many documents.

Expected: message `✅ Index '<index-name>' created (or already exists).`

## Step 3 - Bulk ingest documents
Create or use a JSON Lines file (one JSON object per line) where each line has an `id` field and either a `document` object or other fields. Example file included: `labs/elasticsearch/file.json`.

Example lines:
```json
{"id":"doc-1","document":{"name":"Alice","text":"Alice loves databases"}}
{"id":"doc-2","name":"Bob","text":"Bob studies full text search"}
```

Run:
```bash
python labs/elasticsearch/08_bulk_ingest.py labs/elasticsearch/file.json
```
Expected: a summary message like `✅ Bulk ingest completed. Imported N documents into index='<index-name>'.`

## Step 4 - Search
Run:
```bash
python labs/elasticsearch/09_search.py "search terms here" --top 5
```
Purpose: search the configured index and print ranked results (top N).

Expected: printed ranked results with document id, score, and source.

## Step 5 - Create
Run:
```bash
python labs/elasticsearch/02_create.py
```
Expected: one deterministic student record is created (`id` or key `1001` / `student-1001`).

## Step 6 - Read
Run:
```bash
python labs/elasticsearch/03_read.py
```
Expected: the inserted student values are printed (`Asha`, `DB Basics`).

## Step 7 - Update
Run:
```bash
python labs/elasticsearch/04_update.py
```
Expected: `before` shows original course and `after` shows `Advanced Databases`.

## Step 8 - Delete
Run:
```bash
python labs/elasticsearch/05_delete.py
```
Expected: the target student record is deleted.

## Step 9 - Verify final state
Run:
```bash
python labs/elasticsearch/06_verify.py
```
Expected: verify step confirms the record is absent.

## Common mistakes and fixes
- **Config missing**: fill `.env` and `config/elasticsearch.properties`; scripts print missing keys.
- **Container not ready**: wait 20-60 seconds (Cassandra/Elasticsearch often need more time) and retry Step 1.
- **Wrong port/host**: compare your config with `docker compose ps`.

## Checkpoint questions
1. Which connection values came from environment variables?
2. What deterministic ID/key did this lab use?
3. Which step proves deletion happened successfully?
