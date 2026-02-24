#!/bin/bash

# Auto backup script for ~/.openclaw repository
# Run daily via cron at 20:00

set -e

# Ensure cron can find git and other tools
export PATH="/usr/local/bin:/opt/homebrew/bin:$PATH"

# Configuration
REPO_DIR="$HOME/.openclaw"
LOG_FILE="$REPO_DIR/logs/backup.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
COMMIT_MSG="chore: auto-backup $TIMESTAMP"

# Ensure logs directory exists
mkdir -p "$REPO_DIR/logs"

# Ensure we're in the repo directory
cd "$REPO_DIR" || {
    echo "[$TIMESTAMP] ERROR: Cannot cd to $REPO_DIR" >> "$LOG_FILE"
    exit 1
}

# Check if there are any changes to commit
if git status --porcelain | grep -q '.'; then
    echo "[$TIMESTAMP] Changes detected, creating backup..." >> "$LOG_FILE"
    
    # Add all changes
    git add . >> "$LOG_FILE" 2>&1
    
    # Commit with timestamp
    git commit -m "$COMMIT_MSG" >> "$LOG_FILE" 2>&1
    
    # Push to remote
    if git push origin main >> "$LOG_FILE" 2>&1; then
        echo "[$TIMESTAMP] Backup completed successfully" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] ERROR: git push failed" >> "$LOG_FILE"
        exit 1
    fi
else
    echo "[$TIMESTAMP] No changes to commit" >> "$LOG_FILE"
fi