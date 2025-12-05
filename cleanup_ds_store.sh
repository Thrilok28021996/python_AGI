#!/bin/bash

# Cleanup Script for .DS_Store Files
# This script removes all .DS_Store files from the project and prevents them from being recreated

echo "🧹 Cleaning up .DS_Store files..."
echo ""

# Count existing .DS_Store files
DS_STORE_COUNT=$(find . -name ".DS_Store" -type f 2>/dev/null | wc -l | tr -d ' ')

if [ "$DS_STORE_COUNT" -eq 0 ]; then
    echo "✅ No .DS_Store files found. Your project is clean!"
    echo ""
else
    echo "Found $DS_STORE_COUNT .DS_Store file(s)"
    echo ""

    # Show which files will be deleted
    echo "Files to be deleted:"
    find . -name ".DS_Store" -type f 2>/dev/null
    echo ""

    # Remove all .DS_Store files
    find . -name ".DS_Store" -type f -delete 2>/dev/null

    echo "✅ Deleted $DS_STORE_COUNT .DS_Store file(s)"
    echo ""
fi

# Check if .DS_Store is in .gitignore
if grep -q "^\.DS_Store" .gitignore 2>/dev/null; then
    echo "✅ .DS_Store is already in .gitignore"
else
    echo "⚠️  .DS_Store is NOT in .gitignore"
    echo "   Run: echo '.DS_Store' >> .gitignore"
fi

echo ""
echo "📝 To prevent .DS_Store files system-wide, run:"
echo "   defaults write com.apple.desktopservices DSDontWriteNetworkStores true"
echo ""
echo "🎉 Cleanup complete!"
