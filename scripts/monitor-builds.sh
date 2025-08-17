#!/bin/bash

# GPT-Tokenizer Build Monitor
# This script helps monitor the status of your repository and builds

echo "🚀 GPT-Tokenizer Build Monitor"
echo "================================"
echo ""

# Check current git status
echo "📋 Current Repository Status:"
echo "-------------------------------"
git status --porcelain | while read -r line; do
    if [ -n "$line" ]; then
        echo "   📝 $line"
    fi
done

if [ -z "$(git status --porcelain)" ]; then
    echo "   ✅ Working tree is clean"
fi

echo ""

# Show recent commits
echo "📚 Recent Commits:"
echo "-------------------"
git log --oneline -5 --graph --decorate

echo ""

# Check if GitHub Actions workflow exists
if [ -f ".github/workflows/deploy-pages.yml" ]; then
    echo "✅ GitHub Actions workflow found:"
    echo "   📁 .github/workflows/deploy-pages.yml"
    echo "   🔄 Will trigger on commits to main branch"
else
    echo "❌ GitHub Actions workflow not found"
fi

echo ""

# Check if docs template exists
if [ -f "docs-template.html" ]; then
    echo "✅ HTML template found:"
    echo "   📁 docs-template.html"
else
    echo "❌ HTML template not found"
fi

echo ""

# Show next steps
echo "🎯 Next Steps to Enable GitHub Pages:"
echo "--------------------------------------"
echo "1. Commit and push these changes:"
echo "   git add ."
echo "   git commit -m 'Add GitHub Pages automation'"
echo "   git push origin main"
echo ""
echo "2. Go to GitHub repository Settings → Pages"
echo "3. Select 'GitHub Actions' as source"
echo "4. Monitor builds in Actions tab"
echo ""

# Check if there are uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
    echo "⚠️  You have uncommitted changes!"
    echo "   Run 'git add .' and 'git commit' to save them"
    echo "   Then 'git push origin main' to trigger the build"
else
    echo "✅ No uncommitted changes"
    echo "   Run 'git push origin main' to trigger a build (if you have remote changes)"
fi

echo ""
echo "🔍 To monitor builds in real-time:"
echo "   - Go to GitHub → Actions tab"
echo "   - Or use: gh run list (if GitHub CLI is installed)"
echo ""
echo "📊 Build Status:"
echo "   🟢 Success: Build completed successfully"
echo "   🟡 Running: Build is currently in progress"
echo "   🔴 Failed: Build encountered an error"
echo "   ⚪ Cancelled: Build was cancelled"
