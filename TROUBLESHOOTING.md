# Troubleshooting Guide

## Common Issues and Solutions

### 🔴 `view_advanced_docs.sh` hangs or doesn't load

**Problem**: Port 8080 is already in use by the basic example's docs server.

**Solution**: The scripts now use different ports:
- Basic example: `http://localhost:8080` (run with `./view_docs.sh`)
- Advanced example: `http://localhost:8081` (run with `./view_advanced_docs.sh`)

**Manual fix** if still having issues:
```bash
# Find and kill existing dbt docs serve processes
ps aux | grep "dbt docs serve" | grep -v grep
kill <PID>  # Replace <PID> with the process ID

# Then run the script again
./view_advanced_docs.sh
```

---

### 🔴 Models fail to build with "Catalog Error"

**Problem**: DuckDB can't find the seed tables.

**Solution**: Make sure you run `dbt seed` before `dbt run`:
```bash
cd lineage_demo  # or lineage_advanced
dbt seed
dbt run
```

Or use the convenience scripts:
```bash
./run_basic_example.sh      # Does everything for basic
./run_advanced_example.sh   # Does everything for advanced
```

---

### 🔴 "Manifest not found" when generating visualizations

**Problem**: dbt hasn't generated the manifest.json file yet.

**Solution**: Run `dbt docs generate` first:
```bash
cd lineage_demo  # or lineage_advanced
dbt docs generate
cd ..
python visualize_lineage.py  # or visualize_lineage_advanced.py
```

---

### 🔴 Tests are failing in advanced example

**Problem**: This is expected! The demo data is intentionally small and may not satisfy all test conditions.

**Solution**: Tests failing is normal for demo data. To run models without tests:
```bash
cd lineage_advanced
dbt run  # Runs models only
dbt test  # Runs tests separately (some may fail)
```

To see which tests failed:
```bash
dbt test --store-failures
```

---

### 🔴 Virtual environment activation fails

**Problem**: Virtual environment wasn't created or is corrupted.

**Solution**: Recreate the virtual environment:
```bash
cd /Users/raminmoradi/Repos/test-dbt
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install dbt-core dbt-duckdb networkx matplotlib
```

---

### 🔴 Both docs servers running at the same time

**You can run both!** They use different ports:
- Basic: `http://localhost:8080`
- Advanced: `http://localhost:8081`

Open two terminal windows:
```bash
# Terminal 1
./view_docs.sh

# Terminal 2
./view_advanced_docs.sh
```

Then open both in your browser:
- http://localhost:8080 (basic)
- http://localhost:8081 (advanced)

---

### 🔴 Port already in use

**Problem**: Another application is using port 8080 or 8081.

**Solution**: Use a different port:
```bash
cd lineage_demo
dbt docs serve --port 8082  # Use any available port
```

Or kill the process using that port:
```bash
lsof -i :8080  # Find what's using port 8080
kill <PID>
```

---

### 🔴 Visualization script errors

**Problem**: Missing Python packages.

**Solution**: Ensure all packages are installed:
```bash
source venv/bin/activate
pip install networkx matplotlib
python visualize_lineage.py
```

---

### 🔴 "No such file or directory" when running scripts

**Problem**: Scripts aren't executable or you're in the wrong directory.

**Solution**: 
```bash
# Make scripts executable
chmod +x *.sh

# Ensure you're in the project root
cd /Users/raminmoradi/Repos/test-dbt
./run_basic_example.sh
```

---

### 🔴 DuckDB database is locked

**Problem**: Database file is locked by another process.

**Solution**: Close any DuckDB connections:
```bash
# Find processes using the database
lsof | grep dev.duckdb

# Or just remove and rebuild
cd lineage_demo
rm dev.duckdb
dbt seed
dbt run
```

---

### 🔴 Incremental model not working as expected

**Problem**: First run of incremental model creates full table.

**Solution**: This is normal! Incremental models work like this:
- **First run**: Creates full table
- **Subsequent runs**: Only processes new data

To see incremental behavior:
```bash
cd lineage_advanced
dbt run --models fct_financial_metrics  # Full refresh
dbt run --models fct_financial_metrics  # Incremental (no new data)

# Force full refresh
dbt run --models fct_financial_metrics --full-refresh
```

---

### 🔴 Snapshot not capturing changes

**Problem**: Snapshot only captures changes, not all rows every time.

**Solution**: This is expected behavior. To see snapshot in action:
1. Run snapshot: `dbt snapshot`
2. Modify seed data in `raw_patients.csv` (change insurance_provider for a patient)
3. Re-run seed: `dbt seed --full-refresh`
4. Run snapshot again: `dbt snapshot`
5. Query snapshot table to see versioning:
```sql
-- In DuckDB
SELECT * FROM snapshots.snap_patient_insurance 
WHERE patient_id = 1001
ORDER BY dbt_valid_from;
```

---

## Quick Fixes

### Clean Everything and Start Fresh

**Basic Example:**
```bash
cd lineage_demo
dbt clean
rm dev.duckdb
dbt seed
dbt run
dbt docs generate
```

**Advanced Example:**
```bash
cd lineage_advanced
dbt clean
rm dev.duckdb
dbt seed
dbt run
dbt snapshot
dbt docs generate
```

### Regenerate All Visualizations

```bash
cd /Users/raminmoradi/Repos/test-dbt
python visualize_lineage.py
python visualize_lineage_advanced.py
python visualize_lineage_html.py
```

---

## Getting Help

### Check dbt Logs
```bash
cat lineage_demo/logs/dbt.log  # Basic
cat lineage_advanced/logs/dbt.log  # Advanced
```

### Verbose Mode
```bash
dbt run --debug  # See detailed execution
dbt test --debug  # Debug test failures
```

### List All Models
```bash
dbt list  # See all models, seeds, tests
dbt list --select staging.*  # Only staging models
```

---

## Port Reference

| Service | Port | URL |
|---------|------|-----|
| Basic dbt docs | 8080 | http://localhost:8080 |
| Advanced dbt docs | 8081 | http://localhost:8081 |

---

## Still Having Issues?

1. **Check the logs**: `cat lineage_*/logs/dbt.log`
2. **Try clean rebuild**: See "Clean Everything and Start Fresh" above
3. **Verify installation**: `dbt --version`
4. **Check Python version**: `python --version` (should be 3.9+)
5. **Read documentation**: Open `00_START_HERE.md` or `EXAMPLES_GUIDE.md`

---

**Most issues can be solved by running the convenience scripts:**
```bash
./run_basic_example.sh
./run_advanced_example.sh
```

These scripts do everything in the correct order!

