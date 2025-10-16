# 🎯 START HERE

Welcome to your **dbt Data Lineage Visualization** project with **TWO COMPLETE EXAMPLES**!

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

## ⚡ Quick Start (30 seconds)

```bash
# View basic example lineage
open data_lineage.png

# View advanced example lineage
open data_lineage_advanced.png

# Or run examples from scratch
./run_basic_example.sh      # Simple e-commerce (13 nodes)
./run_advanced_example.sh   # Complex healthcare (86+ nodes)
```

## 📚 Documentation

| File | Purpose |
|------|---------|
| **📖 README.md** | Complete project documentation |
| **🚀 EXAMPLES_GUIDE.md** | Detailed guide for both examples |
| **🔧 DBT_FEATURES.md** | All dbt features explained |
| **📄 This file** | Quick start guide |

## 🎨 What's Included

### Example 1: Basic (E-Commerce)
- **Domain**: Online retail (customers, orders, products)
- **Complexity**: Beginner-friendly
- **Nodes**: 13 (4 seeds + 9 models)
- **Features**: Basic dbt patterns
- **Purpose**: Learn dbt fundamentals

### Example 2: Advanced (Healthcare)
- **Domain**: Hospital management system
- **Complexity**: Production-ready
- **Nodes**: 86+ (9 sources + 9 seeds + 18 models + 1 snapshot + 49 tests)
- **Features**: All major dbt features
- **Purpose**: Real-world patterns

## 🏃 Running Examples

### Basic Example
```bash
./run_basic_example.sh
open data_lineage.png
./view_docs.sh  # Interactive docs on http://localhost:8080
```

### Advanced Example
```bash
./run_advanced_example.sh
open data_lineage_advanced.png
./view_advanced_docs.sh  # Interactive docs on http://localhost:8081
```

**Note**: Both can run simultaneously on different ports!

## 📊 Visualizations

Each example generates 3 types of visualizations:

1. **Static PNG** - High-quality diagram for presentations
2. **Interactive HTML** - Web-based, zoomable, clickable
3. **dbt Docs** - Full documentation with SQL code

## 🎓 Learning Path

1. **Start here**: Open `data_lineage.png` to see basic lineage
2. **Read**: `EXAMPLES_GUIDE.md` for detailed walkthrough
3. **Run**: `./run_basic_example.sh` to build from scratch
4. **Explore**: `./view_docs.sh` for interactive exploration
5. **Advance**: `./run_advanced_example.sh` for complex patterns
6. **Deep dive**: `DBT_FEATURES.md` for feature explanations

## 🔑 Key Files

```
test-dbt/
├── 00_START_HERE.md              ← You are here
├── README.md                     ← Full documentation
├── EXAMPLES_GUIDE.md             ← Example walkthroughs
├── DBT_FEATURES.md               ← Feature explanations
│
├── lineage_demo/                 ← Basic example
│   ├── seeds/                    ← 4 CSV files
│   ├── models/                   ← 9 SQL models
│   └── dev.duckdb                ← Database
│
├── lineage_advanced/             ← Advanced example
│   ├── seeds/                    ← 9 CSV files
│   ├── models/                   ← 18 SQL models
│   ├── macros/                   ← 2 custom macros
│   ├── snapshots/                ← 1 SCD Type 2 snapshot
│   └── dev.duckdb                ← Database
│
├── Scripts:
│   ├── run_basic_example.sh      ← Build basic
│   ├── run_advanced_example.sh   ← Build advanced
│   ├── view_docs.sh              ← View basic docs
│   └── view_advanced_docs.sh     ← View advanced docs
│
└── Generated:
    ├── data_lineage.png          ← Basic lineage
    └── data_lineage_advanced.png ← Advanced lineage
```

## 💡 What Makes This Special

### Two Complete Examples
Most tutorials show only one example. You get:
- **Basic**: Learn fundamentals
- **Advanced**: See production patterns

### Every Major dbt Feature
The advanced example demonstrates:
- ✅ Sources (explicit source definitions)
- ✅ Tests (49 data quality checks)
- ✅ Macros (reusable SQL functions)
- ✅ Snapshots (historical tracking)
- ✅ Incremental models (performance optimization)
- ✅ Comprehensive documentation
- ✅ Layered architecture

### Run Examples Independently
Each example is completely self-contained:
- Separate databases
- Independent scripts
- No conflicts

### Multiple Visualization Types
- PNG for presentations
- HTML for exploration
- dbt docs for development

## 🚀 Next Steps

1. **View the lineages**: 
   ```bash
   open data_lineage.png
   open data_lineage_advanced.png
   ```

2. **Read the guide**:
   ```bash
   open EXAMPLES_GUIDE.md
   ```

3. **Explore interactively**:
   ```bash
   ./view_docs.sh
   ```

4. **Modify and rebuild**:
   - Edit any `.sql` file in `lineage_demo/models/`
   - Run `./run_basic_example.sh`
   - See your changes in the lineage!

## 🎯 Goals Achieved

✅ Virtual environment with dbt-core installed  
✅ Two complete dbt projects  
✅ Mock datasets (4 basic + 9 advanced)  
✅ Comprehensive data models (9 + 18 models)  
✅ All major dbt features demonstrated  
✅ Multiple visualization formats  
✅ Independent run scripts  
✅ Complete documentation  

## 📬 What to Explore

### For Beginners
1. Open `data_lineage.png`
2. Read `EXAMPLES_GUIDE.md` → Basic Example section
3. Run `./run_basic_example.sh`
4. Explore `lineage_demo/models/` SQL files

### For Advanced Users
1. Open `data_lineage_advanced.png`
2. Read `DBT_FEATURES.md`
3. Run `./run_advanced_example.sh`
4. Explore `lineage_advanced/models/` and `lineage_advanced/macros/`

### For Production Use
1. Study advanced example structure
2. Copy patterns to your project
3. Adapt to your data sources
4. Add your business logic

---

**Ready to dive in?** Start with: `open data_lineage.png` 🎉

**Need help?** Read: `EXAMPLES_GUIDE.md`

**Want to learn all features?** See: `DBT_FEATURES.md`

