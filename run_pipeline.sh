#!/usr/bin/env bash

# Stop if any command fails
set -euo pipefail

# Set project directories
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

DEV_DIR="$PROJECT_DIR/dev"
PROD_DIR="$PROJECT_DIR/production"

# Enter development directory
cd "$DEV_DIR"

echo "Step 1: Inspecting database..."
python inspect-database.py

echo "Step 2: Running pipeline tests..."
python test-pipeline.py

# Record changelog position before the update
touch changelog.log
OLD_LINES=$(wc -l < changelog.log)

echo "Step 3: Running update pipeline..."
python update-pipeline.py

# Capture only new changelog entries
NEW_ENTRIES=$(tail -n +"$((OLD_LINES + 1))" changelog.log)

# Deploy only if new rows were added
if printf '%s\n' "$NEW_ENTRIES" | grep -q "Database updated."; then

    echo "New data detected. Deploying database..."

    mkdir -p "$PROD_DIR"
    cp cleaned-cademycode-GitHub.db "$PROD_DIR/"

    echo "Production database updated."

else

    echo "No new data added. Production database unchanged."

fi

echo "Pipeline completed successfully."