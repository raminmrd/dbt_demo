# Examples Guide

## Quick Reference

| Example | Script | Docs | Visualization |
|---------|--------|------|---------------|
| Basic (E-commerce) | `./run_basic_example.sh` | `./view_docs.sh` | `data_lineage.png` |
| Advanced (Healthcare) | `./run_advanced_example.sh` | `./view_advanced_docs.sh` | `data_lineage_advanced.png` |

## Basic Example (E-Commerce)

**Run**: `./run_basic_example.sh`  
**View**: `open data_lineage.png`  
**Docs**: `./view_docs.sh` (http://localhost:8080)

**Data**: 4 seeds → 9 models (13 nodes total)  
**Pattern**: Seeds → Staging → Intermediate → Marts

## Advanced Example (Healthcare)

**Run**: `./run_advanced_example.sh`  
**View**: `open data_lineage_advanced.png`  
**Docs**: `./view_advanced_docs.sh` (http://localhost:8081)

**Data**: 9 sources + 9 seeds + 18 models + 1 snapshot + 49 tests (86+ nodes)  
**Features**: Sources, tests, macros, snapshots, incremental models

## Troubleshooting

**Models not building?**
```bash
cd lineage_demo  # or lineage_advanced
dbt clean
dbt seed
dbt run
```

**Tests failing?** (Normal for demo data)
```bash
dbt run  # Models only
dbt test  # Tests separately
```

