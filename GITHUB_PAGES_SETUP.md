# GitHub Pages Setup Guide

This guide explains how to enable GitHub Pages for automatic documentation deployment.

## 🚀 Enable GitHub Pages

### Step 1: Go to Repository Settings

1. Navigate to your repository on GitHub
2. Click the **Settings** tab
3. Scroll down to the **Pages** section

### Step 2: Configure Source

1. **Source**: Select "GitHub Actions"
2. Click **Save**

### Step 3: Wait for Deployment

- The GitHub Actions workflow will automatically deploy your documentation
- Your site will be available at: `https://yourusername.github.io/gpt-tokenizer`
- First deployment may take a few minutes

## ✅ That's It!

Your documentation will now be automatically published to GitHub Pages with every commit to the `main` branch.

## 🔍 Verify Setup

1. **Check Actions Tab**: Look for successful deployments
2. **Visit Your Site**: Go to the URL shown in Pages settings
3. **Test Updates**: Make a small change and push to see automatic updates

## 🚨 Troubleshooting

### Pages Not Showing?

- Check that you selected "GitHub Actions" as the source
- Ensure your repository is public (or you have GitHub Pro for private repos)
- Wait a few minutes for the first deployment

### Build Failures?

- Check the Actions tab for error logs
- Verify all files exist and are accessible
- Check that the workflow file is properly formatted

## 🌟 Benefits

- **Completely Free** - No hosting costs
- **Automatic Updates** - Deploys on every commit
- **Global CDN** - Fast loading worldwide
- **HTTPS** - Automatic SSL certificates
- **Version Control** - Full Git history and rollback

---

**Need help?** Check the [GitHub Pages documentation](https://docs.github.com/en/pages) or create an issue in your repository.
