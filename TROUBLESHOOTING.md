# Troubleshooting

## Common Issues

**Port conflicts**
- Basic docs: http://localhost:8080
- Advanced docs: http://localhost:8081

**Models fail to build**
```bash
cd lineage_demo  # or lineage_advanced
dbt clean
dbt seed
dbt run
```

**Tests failing** (Normal for demo data)
```bash
dbt run  # Models only
dbt test  # Tests separately
```

**Clean rebuild**
```bash
cd lineage_demo  # or lineage_advanced
dbt clean
rm dev.duckdb
dbt seed
dbt run
dbt docs generate
```

