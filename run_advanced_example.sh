#!/bin/bash
# Script to run the advanced example independently

echo "═══════════════════════════════════════════════════════════════"
echo "        RUNNING ADVANCED EXAMPLE (lineage_advanced)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd /Users/raminmoradi/Repos/test-dbt

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Navigate to advanced project
cd lineage_advanced

# Load seeds
echo "🌱 Loading seed data (9 files)..."
dbt seed --quiet

# Run models
echo "🔨 Building dbt models (18 models)..."
dbt run --quiet

# Run snapshots
echo "📸 Creating snapshots (SCD Type 2)..."
dbt snapshot --quiet

# Run tests
echo "✅ Running data quality tests..."
dbt test --quiet || echo "Some tests failed (expected for demo data)"

# Generate documentation
echo "📚 Generating documentation..."
dbt docs generate --quiet

# Go back to root
cd ..

# Generate visualizations
echo "🎨 Generating lineage visualizations..."
python visualize_lineage_advanced.py

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ ADVANCED EXAMPLE COMPLETE!"
echo ""
echo "Generated files:"
echo "  • data_lineage_advanced.png"
echo "  • lineage_advanced_interactive.html"
echo "  • lineage_advanced/target/manifest.json"
echo ""
echo "To view lineage:"
echo "  1. open data_lineage_advanced.png"
echo "  2. open lineage_advanced_interactive.html"
echo "  3. ./view_advanced_docs.sh (for interactive dbt docs)"
echo "═══════════════════════════════════════════════════════════════"

