#!/bin/bash
# Script to run the basic (demo) example independently

echo "═══════════════════════════════════════════════════════════════"
echo "         RUNNING BASIC EXAMPLE (lineage_demo)"
echo "═══════════════════════════════════════════════════════════════"
echo ""

cd /Users/raminmoradi/Repos/test-dbt

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Navigate to basic project
cd lineage_demo

# Load seeds
echo "🌱 Loading seed data..."
dbt seed --quiet

# Run models
echo "🔨 Building dbt models..."
dbt run --quiet

# Generate documentation
echo "📚 Generating documentation..."
dbt docs generate --quiet

# Go back to root
cd ..

# Generate visualizations
echo "🎨 Generating lineage visualizations..."
python visualize_lineage.py

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ BASIC EXAMPLE COMPLETE!"
echo ""
echo "Generated files:"
echo "  • data_lineage.png"
echo "  • lineage_interactive.html"
echo "  • lineage_demo/target/manifest.json"
echo ""
echo "To view lineage:"
echo "  1. open data_lineage.png"
echo "  2. open lineage_interactive.html"
echo "  3. ./view_docs.sh (for interactive dbt docs)"
echo "═══════════════════════════════════════════════════════════════"

