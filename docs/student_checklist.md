# Student Evidence Checklist

Use this worksheet while running each mini-lab. Add screenshots or terminal output snippets as evidence.

## Setup evidence
- [ ] `docker compose up -d` completed
- [ ] Virtual environment created and dependencies installed
- [ ] `.env` configured (without committing secrets)
- [ ] Relevant `config/<db>.properties` reviewed/updated

## PostgreSQL (Relational)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## MongoDB (Document)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## Redis (Key-Value)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## Neo4j (Graph)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## Cassandra (Wide-Column)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## Elasticsearch (Search)
- [ ] 01_connect successful
- [ ] 02_create successful
- [ ] 03_read shows expected record
- [ ] 04_update shows before/after
- [ ] 05_delete successful
- [ ] 06_verify confirms deleted state

## Reflection
- [ ] I can explain why credentials should not be hardcoded
- [ ] I can explain env var override vs properties file values
- [ ] I can identify one use case for each database category
