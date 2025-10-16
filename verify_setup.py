#!/usr/bin/env python3
"""
Setup Verification Script

Verifies that the dbt lineage visualization project is set up correctly.
"""

import os
import sys
from pathlib import Path


def check_file(path, description):
    """Check if a file exists."""
    if Path(path).exists():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False


def check_directory(path, description):
    """Check if a directory exists."""
    if Path(path).is_dir():
        print(f"✓ {description}: {path}")
        return True
    else:
        print(f"✗ {description}: {path} (NOT FOUND)")
        return False


def count_files(directory, pattern):
    """Count files matching a pattern in a directory."""
    return len(list(Path(directory).glob(pattern)))


def main():
    print("="*70)
    print("DBT DATA LINEAGE VISUALIZATION - SETUP VERIFICATION")
    print("="*70)
    print()
    
    all_good = True
    
    # Check virtual environment
    print("📦 Virtual Environment:")
    all_good &= check_directory("venv", "Virtual environment")
    all_good &= check_file("venv/bin/activate", "Activation script")
    print()
    
    # Check dbt project
    print("🏗️  dbt Project:")
    all_good &= check_directory("lineage_demo", "dbt project directory")
    all_good &= check_file("lineage_demo/dbt_project.yml", "dbt config")
    all_good &= check_directory("lineage_demo/models", "Models directory")
    all_good &= check_directory("lineage_demo/seeds", "Seeds directory")
    print()
    
    # Check seeds
    print("🌱 Seed Files:")
    seed_count = count_files("lineage_demo/seeds", "*.csv")
    print(f"   Found {seed_count} seed files")
    all_good &= check_file("lineage_demo/seeds/raw_customers.csv", "Customers")
    all_good &= check_file("lineage_demo/seeds/raw_orders.csv", "Orders")
    all_good &= check_file("lineage_demo/seeds/raw_products.csv", "Products")
    all_good &= check_file("lineage_demo/seeds/raw_order_items.csv", "Order items")
    print()
    
    # Check models
    print("📊 dbt Models:")
    
    print("   Staging Layer:")
    staging_count = count_files("lineage_demo/models/staging", "*.sql")
    print(f"      {staging_count} models")
    
    print("   Intermediate Layer:")
    int_count = count_files("lineage_demo/models/intermediate", "*.sql")
    print(f"      {int_count} models")
    
    print("   Marts Layer:")
    marts_count = count_files("lineage_demo/models/marts", "*.sql")
    print(f"      {marts_count} models")
    
    total_models = staging_count + int_count + marts_count
    print(f"   Total: {total_models} models")
    print()
    
    # Check database
    print("🗄️  Database:")
    all_good &= check_file("lineage_demo/dev.duckdb", "DuckDB database")
    print()
    
    # Check manifest
    print("📋 dbt Artifacts:")
    all_good &= check_directory("lineage_demo/target", "Target directory")
    all_good &= check_file("lineage_demo/target/manifest.json", "Manifest (lineage metadata)")
    print()
    
    # Check visualization scripts
    print("🎨 Visualization Scripts:")
    all_good &= check_file("visualize_lineage.py", "PNG visualization script")
    all_good &= check_file("visualize_lineage_html.py", "HTML visualization script")
    all_good &= check_file("view_docs.sh", "dbt docs server script")
    print()
    
    # Check generated visualizations
    print("🖼️  Generated Visualizations:")
    all_good &= check_file("data_lineage.png", "Static PNG visualization")
    all_good &= check_file("lineage_interactive.html", "Interactive HTML visualization")
    print()
    
    # Check documentation
    print("📚 Documentation:")
    all_good &= check_file("README.md", "Main README")
    all_good &= check_file("QUICKSTART.md", "Quick start guide")
    print()
    
    # Summary
    print("="*70)
    if all_good:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("Your dbt lineage visualization project is ready to use!")
        print()
        print("Next steps:")
        print("  1. View data_lineage.png for static visualization")
        print("  2. Open lineage_interactive.html in your browser")
        print("  3. Run ./view_docs.sh to launch dbt's documentation server")
        print("  4. Read QUICKSTART.md for usage instructions")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Some files are missing. This might be normal if you haven't")
        print("run all the setup steps yet.")
    print("="*70)
    
    # Additional stats
    print()
    print("📈 Project Statistics:")
    print(f"   • {seed_count} seed files (raw data)")
    print(f"   • {total_models} transformation models")
    print(f"   • 3 layers: staging → intermediate → marts")
    print(f"   • 2 visualization outputs generated")
    
    # Check if we can import required packages
    print()
    print("🐍 Python Dependencies:")
    try:
        import dbt
        print(f"   ✓ dbt-core installed")
    except ImportError:
        print(f"   ✗ dbt-core not found")
    
    try:
        import duckdb
        print(f"   ✓ duckdb installed")
    except ImportError:
        print(f"   ✗ duckdb not found")
    
    try:
        import networkx
        print(f"   ✓ networkx installed")
    except ImportError:
        print(f"   ✗ networkx not found")
    
    try:
        import matplotlib
        print(f"   ✓ matplotlib installed")
    except ImportError:
        print(f"   ✗ matplotlib not found")
    
    print()
    print("="*70)


if __name__ == '__main__':
    main()

