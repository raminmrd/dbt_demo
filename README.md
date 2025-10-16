# dbt Data Lineage Visualization

This project demonstrates data lineage visualization using dbt-core with DuckDB, featuring **TWO COMPLETE EXAMPLES**:

1. **BASIC EXAMPLE** (`lineage_demo`) - Simple e-commerce pipeline
2. **ADVANCED EXAMPLE** (`lineage_advanced`) - Complex healthcare system with advanced dbt features

## 📊 Overview

### Example 1: Basic E-Commerce (lineage_demo)
- **4 seeds**: Customer, order, product, and order item data
- **9 models**: Across staging, intermediate, and marts layers
- **13 nodes** total in lineage graph

### Example 2: Advanced Healthcare (lineage_advanced)
- **9 seeds**: Patients, doctors, hospitals, appointments, diagnoses, medications, prescriptions, lab tests, insurance claims
- **18 models**: Complex transformations across multiple layers
- **1 snapshot**: Tracks patient insurance changes over time (SCD Type 2)
- **2 macros**: Reusable SQL functions
- **49 tests**: Data quality validations
- **9 sources**: Explicit source definitions
- **Incremental model**: For efficient large-scale processing
- **86+ nodes** total in lineage graph (including tests)

## ⚙️ Setup (First Time Only)

After cloning, create dbt profiles:

```bash
mkdir -p ~/.dbt
cat > ~/.dbt/profiles.yml << 'EOF'
lineage_demo:
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
  target: dev

lineage_advanced:
  outputs:
    dev:
      type: duckdb
      path: dev.duckdb
  target: dev
EOF
```

Install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb networkx matplotlib
```

## 🚀 Quick Start

### Run Examples Independently

```bash
# Run BASIC example (e-commerce)
./run_basic_example.sh

# Run ADVANCED example (healthcare)
./run_advanced_example.sh
```

### View Interactive Documentation

```bash
# View basic example docs
./view_docs.sh

# View advanced example docs
./view_advanced_docs.sh
```

### Environment

All dependencies are pre-installed in the virtual environment:
- `dbt-core 1.10.13` - Data transformation framework
- `dbt-duckdb` - DuckDB adapter
- `networkx` - Graph analysis
- `matplotlib` - Visualization

## 📁 Project Structure

```
test-dbt/
├── venv/                                    # Virtual environment
│
├── lineage_demo/                            # BASIC EXAMPLE
│   ├── seeds/                              # 4 CSV files
│   ├── models/
│   │   ├── staging/                        # 4 models
│   │   ├── intermediate/                   # 2 models
│   │   └── marts/                          # 3 models
│   ├── target/manifest.json
│   └── dev.duckdb
│
├── lineage_advanced/                        # ADVANCED EXAMPLE
│   ├── seeds/                              # 9 CSV files (healthcare data)
│   ├── models/
│   │   ├── sources.yml                     # Source definitions
│   │   ├── staging/                        # 9 models + tests
│   │   ├── intermediate/                   # 4 models
│   │   └── marts/                          # 5 models (inc. incremental)
│   ├── macros/                             # 2 custom macros
│   ├── snapshots/                          # 1 snapshot (SCD Type 2)
│   ├── target/manifest.json
│   └── dev.duckdb
│
├── Scripts:
│   ├── run_basic_example.sh                # Run basic example
│   ├── run_advanced_example.sh             # Run advanced example
│   ├── view_docs.sh                        # View basic docs
│   ├── view_advanced_docs.sh               # View advanced docs
│   ├── visualize_lineage.py                # Basic visualization
│   ├── visualize_lineage_advanced.py       # Advanced visualization
│   └── visualize_lineage_html.py           # HTML visualization
│
└── Generated Files:
    ├── data_lineage.png                    # Basic PNG
    ├── data_lineage_advanced.png           # Advanced PNG
    ├── lineage_interactive.html            # Basic HTML
    └── lineage_advanced_interactive.html   # Advanced HTML
```

## 🎯 Usage

### 1. Load Seed Data

```bash
cd lineage_demo
dbt seed
```

This loads the CSV files from the `seeds/` directory into DuckDB.

### 2. Run dbt Models

```bash
dbt run
```

This executes all transformation models in the correct order based on dependencies.

### 3. Generate Documentation

```bash
dbt docs generate
```

This creates the `manifest.json` file containing lineage metadata.

### 4. Visualize Lineage

```bash
cd ..
python visualize_lineage.py
```

This generates `data_lineage.png` with a visual representation of your data pipeline.

## 📊 Understanding the Data Models

### Staging Layer
- **Purpose**: Clean and standardize raw data
- **Models**: `stg_customers`, `stg_orders`, `stg_products`, `stg_order_items`
- **Transformations**: Type casting, renaming, basic cleaning

### Intermediate Layer
- **Purpose**: Join and aggregate data for specific use cases
- **int_customer_orders**: Customer-level order metrics
- **int_orders_with_items**: Orders joined with line items and products

### Marts Layer
- **Purpose**: Analytics-ready tables optimized for reporting
- **dim_customers**: Customer dimension with segments
- **fct_orders**: Order-level facts and metrics
- **fct_customer_metrics**: Customer-level KPIs

## 🎨 Lineage Visualization Features

The visualization script provides:

- **Color-coded nodes**:
  - 🟢 Green: Seed files (raw data)
  - 🔵 Blue: dbt models
  - 🟡 Yellow: Sources (if configured)

- **Hierarchical layout**: Shows data flow from left to right
  - Raw Data → Staging → Intermediate → Marts

- **Dependency arrows**: Shows how models depend on each other

- **Summary statistics**: Displays node counts, root nodes, and leaf nodes

## 🔍 Viewing the Lineage

The generated `data_lineage.png` shows:
- 13 total nodes (4 seeds + 9 models)
- 13 edges (dependencies)
- 4 root nodes (seed files)
- 1 leaf node (`fct_customer_metrics`)

## 🛠️ Customization

### Add New Models

1. Create a new SQL file in the appropriate folder:
   ```sql
   -- models/marts/fct_my_model.sql
   with source as (
       select * from {{ ref('int_customer_orders') }}
   )
   select * from source
   ```

2. Run the model:
   ```bash
   dbt run --models fct_my_model
   ```

3. Regenerate lineage:
   ```bash
   dbt docs generate
   python visualize_lineage.py
   ```

### Modify Visualization

Edit `visualize_lineage.py` to customize:
- Colors (see `get_node_color()`)
- Layout (modify `pos` calculation)
- Node size, font size, etc.

## 📚 Additional Resources

- [dbt Documentation](https://docs.getdbt.com/)
- [dbt-core GitHub](https://github.com/dbt-labs/dbt-core)
- [DuckDB Documentation](https://duckdb.org/)
- [NetworkX Documentation](https://networkx.org/)

## 🎓 Learning Path

1. **Explore the seed data**: Check the CSV files to understand the raw data
2. **Review staging models**: See how data is cleaned
3. **Study intermediate models**: Understand joins and aggregations
4. **Analyze marts**: Learn about dimensional modeling
5. **Experiment**: Add your own models and transformations

## 💡 Tips

- Use `dbt run --models model_name` to run specific models
- Use `dbt test` to run data quality tests
- Use `dbt docs serve` to view interactive documentation in your browser
- Check `dev.duckdb` file to query the database directly

## 🐛 Troubleshooting

**Issue**: Models fail to run
- **Solution**: Check dependencies with `dbt list --models model_name+`

**Issue**: Visualization not showing
- **Solution**: Ensure matplotlib has a display backend: `export MPLBACKEND=TkAgg`

**Issue**: Manifest not found
- **Solution**: Run `dbt docs generate` first

## 📝 License

This is a demonstration project for educational purposes.

---

**Created with**: dbt-core 1.10.13 | DuckDB 1.4.1 | Python 3.9

