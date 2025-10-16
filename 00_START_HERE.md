# Quick Start

## ⚙️ Setup (First Time Only)

```bash
# Create dbt profiles
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

# Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb networkx matplotlib
```

## ⚡ Run Examples

```bash
# Basic example (e-commerce)
./run_basic_example.sh
open data_lineage.png

# Advanced example (healthcare) 
./run_advanced_example.sh
open data_lineage_advanced.png
```

## View Documentation

```bash
./view_docs.sh              # Basic docs (http://localhost:8080)
./view_advanced_docs.sh     # Advanced docs (http://localhost:8081)
```

