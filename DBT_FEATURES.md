# dbt Features

## Feature Comparison

| Feature | Basic | Advanced | Purpose |
|---------|-------|----------|---------|
| **Seeds** | ✅ | ✅ | Load CSV data |
| **Models** | ✅ | ✅ | Transform data with SQL |
| **Sources** | ❌ | ✅ | Define raw data sources |
| **Tests** | ❌ | ✅ | Data quality validation |
| **Macros** | ❌ | ✅ | Reusable SQL functions |
| **Snapshots** | ❌ | ✅ | Track historical changes |
| **Incremental** | ❌ | ✅ | Process only new data |

## Key Features

### Seeds
CSV files loaded into database as tables
```sql
select * from {{ ref('raw_customers') }}
```

### Sources  
Define raw data sources with tests
```yaml
sources:
  - name: hospital_raw
    tables:
      - name: raw_patients
        columns:
          - name: patient_id
            tests: [unique, not_null]
```

### Tests
Data quality validation
```yaml
models:
  - name: stg_patients
    columns:
      - name: patient_id
        tests: [unique, not_null]
```

### Macros
Reusable SQL functions
```sql
{{ calculate_age('date_of_birth') }}
```

### Snapshots
Track historical changes (SCD Type 2)
```sql
{% snapshot snap_patient_insurance %}
{{ config(unique_key='patient_id', strategy='check') }}
select * from {{ ref('stg_patients') }}
{% endsnapshot %}
```

### Incremental Models
Process only new data
```sql
{{ config(materialized='incremental') }}
select * from claims
{% if is_incremental() %}
where claim_date > (select max(metric_date) from {{ this }})
{% endif %}
```

