# dbt Data Lineage Visualization

Two complete dbt examples with lineage visualization:

1. **BASIC** (`lineage_demo`) - E-commerce pipeline (13 nodes)
2. **ADVANCED** (`lineage_advanced`) - Healthcare system with all dbt features (86+ nodes)

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

```bash
# Run examples
./run_basic_example.sh      # Basic e-commerce
./run_advanced_example.sh   # Advanced healthcare

# View documentation
./view_docs.sh              # Basic docs (port 8080)
./view_advanced_docs.sh     # Advanced docs (port 8081)
```

## 📁 Project Structure

```
test-dbt/
├── lineage_demo/           # Basic example
├── lineage_advanced/       # Advanced example  
├── run_basic_example.sh    # Run basic
├── run_advanced_example.sh # Run advanced
├── view_docs.sh           # Basic docs (8080)
├── view_advanced_docs.sh  # Advanced docs (8081)
└── data_lineage*.png      # Generated visualizations
```

## Generated Files

After running examples, you get:
- `data_lineage.png` - Basic example visualization
- `data_lineage_advanced.png` - Advanced example visualization
- Interactive docs at http://localhost:8080 (basic) and http://localhost:8081 (advanced)

