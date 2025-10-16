# dbt Features Demonstrated

This document outlines the dbt features used in each example and explains their purpose.

## Feature Comparison

| Feature | Basic Example | Advanced Example | Purpose |
|---------|--------------|------------------|---------|
| **Seeds** | ✅ (4 files) | ✅ (9 files) | Load CSV data into database |
| **Models** | ✅ (9 models) | ✅ (18 models) | Transform data with SQL |
| **Sources** | ❌ | ✅ | Explicitly define and test raw data sources |
| **Tests** | ❌ | ✅ (49 tests) | Validate data quality (uniqueness, nulls, relationships, accepted values) |
| **Macros** | ❌ | ✅ (2 macros) | Create reusable SQL functions |
| **Snapshots** | ❌ | ✅ (1 snapshot) | Track historical changes (SCD Type 2) |
| **Incremental Models** | ❌ | ✅ (1 model) | Process only new/changed data efficiently |
| **Documentation** | Minimal | ✅ Comprehensive | Document models, columns, and tests |
| **Ref Function** | ✅ | ✅ | Reference other models (enables lineage tracking) |
| **Layered Architecture** | ✅ | ✅ | Staging → Intermediate → Marts |

## Detailed Feature Explanations

### 1. Seeds
**What**: CSV files that dbt loads into your database as tables  
**When to use**: Small, static reference data (< 1MB)  
**Example**: Customer list, product catalog, status codes

**Basic**: 4 seeds (customers, orders, products, order_items)  
**Advanced**: 9 seeds (patients, doctors, hospitals, appointments, diagnoses, medications, prescriptions, lab_tests, insurance_claims)

```sql
-- After running: dbt seed
-- You can reference seeds in models:
select * from {{ ref('raw_customers') }}
```

---

### 2. Sources
**What**: Explicit definitions of raw data sources in your data warehouse  
**When to use**: When reading from existing database tables (not seeds)  
**Benefits**: 
- Source freshness checks
- Documentation
- Lineage tracking from raw data
- Data quality tests on sources

**Used in**: Advanced example only

```yaml
# models/sources.yml
sources:
  - name: hospital_raw
    description: Raw hospital management system data
    schema: main
    tables:
      - name: raw_patients
        columns:
          - name: patient_id
            tests:
              - unique
              - not_null
```

```sql
-- Reference sources in models:
select * from {{ source('hospital_raw', 'raw_patients') }}
```

---

### 3. Tests
**What**: Data quality assertions that validate your data  
**Types**:
- **Generic tests**: Built-in (unique, not_null, accepted_values, relationships)
- **Singular tests**: Custom SQL queries

**When to use**: Always! Testing ensures data quality and catches issues early

**Used in**: Advanced example (49 tests)

```yaml
# models/staging/staging_schema.yml
models:
  - name: stg_patients
    columns:
      - name: patient_id
        tests:
          - unique
          - not_null
      - name: status
        tests:
          - accepted_values:
              values: ['active', 'inactive']
      - name: doctor_id
        tests:
          - relationships:
              to: ref('stg_doctors')
              field: doctor_id
```

**Run tests**:
```bash
dbt test                    # All tests
dbt test --models stg_*     # Staging tests only
```

---

### 4. Macros
**What**: Reusable Jinja templates that generate SQL  
**When to use**: Repeated SQL logic, dynamic SQL generation  
**Benefits**: DRY (Don't Repeat Yourself), maintainability

**Used in**: Advanced example (2 macros)

```sql
-- macros/calculate_age.sql
{% macro calculate_age(date_of_birth_column) %}
    date_diff('year', {{ date_of_birth_column }}::date, current_date)
{% endmacro %}

-- Use in models:
select
    patient_id,
    {{ calculate_age('date_of_birth') }} as age
from patients
```

---

### 5. Snapshots (Slowly Changing Dimensions Type 2)
**What**: Track historical changes to mutable data  
**When to use**: When you need to preserve history of changing records  
**Strategy**: 
- **Timestamp**: Track changes based on updated_at column
- **Check**: Track changes when specific columns change

**Used in**: Advanced example (patient insurance snapshot)

```sql
-- snapshots/snap_patient_insurance.sql
{% snapshot snap_patient_insurance %}
{{
    config(
      target_schema='snapshots',
      unique_key='patient_id',
      strategy='check',
      check_cols=['insurance_provider'],
    )
}}
select * from {{ ref('stg_patients') }}
{% endsnapshot %}
```

**How it works**:
- First run: Creates snapshot with `dbt_valid_from` and `dbt_valid_to`
- Subsequent runs: Updates `dbt_valid_to` for changed records, inserts new versions

**Run snapshots**:
```bash
dbt snapshot
```

---

### 6. Incremental Models
**What**: Models that process only new or changed data  
**When to use**: Large, append-only datasets (events, logs, transactions)  
**Benefits**: Faster runs, lower compute costs

**Used in**: Advanced example (fct_financial_metrics)

```sql
-- models/marts/fct_financial_metrics.sql
{{ config(
    materialized='incremental',
    unique_key='metric_date'
) }}

select * from claims
{% if is_incremental() %}
    -- Only process new records
    where claim_date > (select max(metric_date) from {{ this }})
{% endif %}
```

**Strategies**:
- **Append**: Add new rows (default)
- **Merge**: Update existing + add new (requires unique_key)
- **Delete+Insert**: Delete old + insert new

---

### 7. Ref Function
**What**: Reference other dbt models  
**Why**: Creates dependency graph for proper execution order and lineage tracking

**Used in**: Both examples

```sql
with customers as (
    select * from {{ ref('stg_customers') }}
),
orders as (
    select * from {{ ref('stg_orders') }}
)
select * from customers
join orders on customers.id = orders.customer_id
```

**Benefits**:
- dbt builds models in the right order
- Lineage graph shows dependencies
- Easy refactoring (rename model, references update automatically)

---

### 8. Documentation
**What**: Descriptions for models, columns, and business logic  
**Where**: schema.yml files  
**View**: `dbt docs generate` then `dbt docs serve`

**Used in**: Advanced example (comprehensive)

```yaml
models:
  - name: dim_patients
    description: Patient dimension table with visit history
    columns:
      - name: patient_id
        description: Primary key - unique patient identifier
      - name: patient_category
        description: Engagement level (Registered, New, Regular, Frequent)
```

---

### 9. Layered Architecture
**What**: Organizing models into logical layers  
**Pattern**: Staging → Intermediate → Marts  
**Benefits**: Clear data flow, easier maintenance, better performance

**Used in**: Both examples

**Layers**:
1. **Staging** (`stg_*`): Clean, standardize, type cast
2. **Intermediate** (`int_*`): Business logic, joins, aggregations
3. **Marts** (`dim_*`, `fct_*`): Final analytics-ready tables

---

## How to Choose Between Examples

### Use BASIC Example When:
- Learning dbt fundamentals
- Simple data pipeline (< 10 sources)
- No historical tracking needed
- Prototype/POC

### Use ADVANCED Example When:
- Production-ready pipeline
- Data quality is critical (use tests)
- Need historical tracking (snapshots)
- Large datasets (incremental models)
- Complex transformations (macros)
- Multiple data sources (sources)

## Additional dbt Features Not Shown

### Available but Not Demonstrated:
- **Exposures**: Track BI dashboards and reports that use dbt models
- **Metrics**: Define business metrics (v1.6+)
- **Packages**: Use community packages (dbt-utils, dbt-expectations)
- **Hooks**: Run SQL before/after models (create indexes, grants, etc.)
- **Tags**: Organize and run subsets of models
- **Custom schemas**: Write models to different schemas
- **Variables**: Pass runtime variables to models
- **Analysis**: Ad-hoc queries that don't create tables
- **Jinja**: Advanced templating for dynamic SQL

## Learning Path

1. **Start with BASIC example**
   - Understand staging → intermediate → marts
   - Learn `ref()` function
   - See lineage visualization

2. **Move to ADVANCED example**
   - Add tests for data quality
   - Use sources for better lineage
   - Create macros for reusable logic
   - Implement snapshots for history
   - Use incremental for performance

3. **Explore More**
   - Read [dbt documentation](https://docs.getdbt.com/)
   - Install [dbt packages](https://hub.getdbt.com/)
   - Join [dbt Community](https://community.getdbt.com/)

---

**Resources**:
- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [dbt Style Guide](https://github.com/dbt-labs/corp/blob/main/dbt_style_guide.md)
- [How we structure our dbt projects](https://docs.getdbt.com/guides/best-practices/how-we-structure/1-guide-overview)

