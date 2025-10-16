#!/bin/bash
# Script to launch dbt documentation server for advanced example

echo "🚀 Starting dbt documentation server for ADVANCED example..."
echo "📝 This will open an interactive documentation viewer in your browser"
echo "   at http://localhost:8081"
echo ""
echo "   You can explore the lineage graph interactively!"
echo ""
echo "   Press Ctrl+C to stop the server when you're done."
echo ""

cd lineage_advanced
source ../venv/bin/activate
dbt docs serve --port 8081

