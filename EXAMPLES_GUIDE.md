# Examples Guide

This project contains **two complete dbt lineage examples** that you can run independently.

## Quick Reference

| Aspect | Basic Example | Advanced Example |
|--------|--------------|------------------|
| **Project Name** | `lineage_demo` | `lineage_advanced` |
| **Domain** | E-commerce | Healthcare |
| **Complexity** | Simple | Complex |
| **Seeds** | 4 | 9 |
| **Models** | 9 | 18 |
| **Total Nodes** | 13 | 86+ (inc. tests) |
| **Features Used** | Basic ref() | All advanced features |
| **Run Script** | `./run_basic_example.sh` | `./run_advanced_example.sh` |
| **Docs Script** | `./view_docs.sh` | `./view_advanced_docs.sh` |
| **Visualization** | `data_lineage.png` | `data_lineage_advanced.png` |

## Example 1: Basic (E-Commerce)

### Purpose
Learn dbt fundamentals and lineage visualization basics

### Data Model
- **Customers**: User accounts
- **Orders**: Purchase transactions  
- **Products**: Items for sale
- **Order Items**: Line items in orders

### Transformations
```
Seeds (4) → Staging (4) → Intermediate (2) → Marts (3)
```

### Key Learnings
- ✅ How to structure a dbt project
- ✅ Staging → Intermediate → Marts pattern
- ✅ Using `ref()` for dependencies
- ✅ Lineage graph visualization
- ✅ Basic data transformations

### Run It
```bash
# One command does everything
./run_basic_example.sh

# Or manually:
cd lineage_demo
dbt seed
dbt run
dbt docs generate
cd ..
python visualize_lineage.py
```

### View Results
- **PNG**: `open data_lineage.png`
- **HTML**: `open lineage_interactive.html`
- **Interactive**: `./view_docs.sh` (opens on http://localhost:8080)

---

## Example 2: Advanced (Healthcare)

### Purpose
Production-ready example demonstrating all major dbt features

### Data Model
- **Patients**: Demographics and contact info
- **Doctors**: Healthcare providers
- **Hospitals**: Facility information
- **Appointments**: Scheduled visits
- **Diagnoses**: Patient diagnoses
- **Medications**: Drug catalog
- **Prescriptions**: Medication orders
- **Lab Tests**: Test results
- **Insurance Claims**: Billing data

### Transformations
```
Sources (9) → Seeds (9) → Staging (9) → Intermediate (4) → Marts (5) + Snapshot (1)
```

### Advanced Features Used

#### 1. Sources (`models/sources.yml`)
```yaml
sources:
  - name: hospital_raw
    tables:
      - name: raw_patients
        columns:
          - name: patient_id
            tests:
              - unique
              - not_null
```

#### 2. Tests (49 total)
- Uniqueness tests
- Not null tests
- Referential integrity
- Accepted values
- Source tests

#### 3. Macros (`macros/`)
```sql
{{ calculate_age('date_of_birth') }}
{{ cents_to_dollars('amount') }}
```

#### 4. Snapshot (`snapshots/snap_patient_insurance.sql`)
Tracks patient insurance changes over time (SCD Type 2)

#### 5. Incremental Model (`marts/fct_financial_metrics.sql`)
Processes only new claims incrementally

#### 6. Comprehensive Documentation
All models and columns documented in schema.yml files

### Key Learnings
- ✅ Source definitions and testing
- ✅ Data quality with tests
- ✅ Reusable SQL with macros
- ✅ Historical tracking with snapshots
- ✅ Performance with incremental models
- ✅ Complex multi-table joins
- ✅ Business logic implementation

### Run It
```bash
# One command does everything
./run_advanced_example.sh

# Or manually:
cd lineage_advanced
dbt seed
dbt run
dbt snapshot
dbt test
dbt docs generate
cd ..
python visualize_lineage_advanced.py
```

### View Results
- **PNG**: `open data_lineage_advanced.png`
- **HTML**: `open lineage_advanced_interactive.html`
- **Interactive**: `./view_advanced_docs.sh` (opens on http://localhost:8081)

---

## Comparison of Lineage Graphs

### Basic Example Lineage
- **Nodes**: 13 (4 seeds + 9 models)
- **Edges**: 13
- **Layers**: 3 (Staging, Intermediate, Marts)
- **Visual**: Clean, easy to understand
- **Use case**: Learning, simple pipelines

### Advanced Example Lineage
- **Nodes**: 86+ (9 sources + 9 seeds + 18 models + 1 snapshot + 49 tests)
- **Edges**: 88+
- **Layers**: 4 (Sources, Staging, Intermediate, Marts, Snapshots)
- **Visual**: Complex, realistic production pipeline
- **Use case**: Production systems, complex analytics

---

## When to Use Each Example

### Use BASIC if you want to:
- ✅ Learn dbt basics quickly
- ✅ Understand lineage visualization
- ✅ See a simple end-to-end pipeline
- ✅ Teach dbt to others
- ✅ Prototype a new project

### Use ADVANCED if you want to:
- ✅ See production-ready dbt patterns
- ✅ Learn advanced dbt features
- ✅ Understand data quality testing
- ✅ Implement historical tracking
- ✅ Handle complex data models
- ✅ See performance optimizations

---

## Exploring the Code

### Basic Example Structure
```
lineage_demo/models/
├── staging/
│   ├── stg_customers.sql        # Clean customers
│   ├── stg_orders.sql           # Clean orders
│   ├── stg_products.sql         # Clean products
│   └── stg_order_items.sql      # Clean order items
├── intermediate/
│   ├── int_customer_orders.sql  # Join customers + orders
│   └── int_orders_with_items.sql # Join orders + items + products
└── marts/
    ├── dim_customers.sql         # Customer dimension
    ├── fct_orders.sql            # Order facts
    └── fct_customer_metrics.sql  # Customer metrics
```

### Advanced Example Structure
```
lineage_advanced/models/
├── sources.yml                    # Source definitions
├── staging/
│   ├── staging_schema.yml        # Tests & docs
│   ├── stg_patients.sql          # Uses calculate_age macro
│   ├── stg_doctors.sql
│   ├── stg_hospitals.sql
│   ├── stg_appointments.sql
│   ├── stg_diagnoses.sql
│   ├── stg_medications.sql
│   ├── stg_prescriptions.sql
│   ├── stg_lab_tests.sql
│   └── stg_insurance_claims.sql
├── intermediate/
│   ├── int_patient_visits.sql    # Multi-table join
│   ├── int_prescriptions_with_costs.sql
│   ├── int_diagnoses_with_context.sql
│   └── int_claim_analysis.sql
└── marts/
    ├── marts_schema.yml          # Tests & docs
    ├── dim_patients.sql          # Patient dimension
    ├── dim_doctors.sql           # Doctor dimension
    ├── fct_appointments.sql      # Appointment facts
    ├── fct_patient_health_summary.sql
    └── fct_financial_metrics.sql # INCREMENTAL model
```

---

## Tips

### Running Both Examples
You can run both examples simultaneously - they use separate databases:
- Basic: `lineage_demo/dev.duckdb`
- Advanced: `lineage_advanced/dev.duckdb`

### Regenerating Visualizations
```bash
# Basic
python visualize_lineage.py

# Advanced
python visualize_lineage_advanced.py

# HTML versions
python visualize_lineage_html.py  # Creates lineage_interactive.html
```

### Exploring the Data
```bash
# Basic example
cd lineage_demo
duckdb dev.duckdb
> SELECT * FROM dim_customers;
> SELECT * FROM fct_orders;

# Advanced example
cd lineage_advanced
duckdb dev.duckdb
> SELECT * FROM dim_patients;
> SELECT * FROM fct_appointments;
> SELECT * FROM snap_patient_insurance; -- Snapshot table
```

### Modifying Examples
1. Edit a model SQL file
2. Run `dbt run --models model_name`
3. Regenerate docs: `dbt docs generate`
4. Regenerate visualization: `python visualize_lineage*.py`

---

## Additional Resources

- **dbt Features Guide**: See `DBT_FEATURES.md` for detailed feature explanations
- **Main README**: See `README.md` for complete documentation
- **dbt Docs**: https://docs.getdbt.com/
- **dbt Community**: https://community.getdbt.com/

---

## Troubleshooting

### Models not building?
```bash
# Clean and rebuild
cd lineage_demo  # or lineage_advanced
dbt clean
dbt seed
dbt run
```

### Tests failing?
```bash
# See which tests failed
dbt test --store-failures

# Skip tests during development
dbt run  # Tests are separate from run
```

### Visualization not generating?
```bash
# Make sure docs are generated first
cd lineage_demo  # or lineage_advanced
dbt docs generate
cd ..
python visualize_lineage.py  # or visualize_lineage_advanced.py
```

---

**Happy exploring!** 🎉

