#!/bin/bash
# Script to launch dbt documentation server

echo "🚀 Starting dbt documentation server for BASIC example..."
echo "📝 This will open an interactive documentation viewer in your browser"
echo "   at http://localhost:8080"
echo ""
echo "   You can explore the lineage graph interactively!"
echo ""
echo "   Press Ctrl+C to stop the server when you're done."
echo ""

cd lineage_demo
source ../venv/bin/activate
dbt docs serve

