#!/bin/bash
# Confluence Setup Script
# Run this after getting your API token

echo "🔧 Confluence CLI Setup"
echo "========================"
echo ""

# Check if already configured
if [ -f ~/.confluence-cli/config.json ]; then
    echo "✅ Already configured:"
    cat ~/.confluence-cli/config.json
    echo ""
    read -p "Reconfigure? (y/n): " reconfigure
    if [ "$reconfigure" != "y" ]; then
        echo "Keeping existing configuration."
        exit 0
    fi
fi

# Get credentials
read -p "Confluence URL (e.g., https://company.atlassian.net/wiki): " CONFLUENCE_URL
read -p "Email: " EMAIL
read -p "API Token: " API_TOKEN

# Initialize
echo ""
echo "📝 Initializing Confluence CLI..."
confluence init --host "$CONFLUENCE_URL" --username "$EMAIL" --password "$API_TOKEN"

# Test connection
echo ""
echo "🔍 Testing connection..."
confluence spaces

echo ""
echo "✅ Setup complete!"
echo ""
echo "Quick commands:"
echo "  confluence spaces              # List all spaces"
echo "  confluence search 'query'      # Search pages"
echo "  confluence read PAGE_ID        # Read page content"
echo "  confluence info PAGE_ID        # Get page info"
