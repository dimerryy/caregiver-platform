# Git Setup Guide

## Initialize Git Repository

```bash
# Initialize git (already done)
git init

# Add all files (respecting .gitignore)
git add .

# Check what will be committed
git status

# Create initial commit
git commit -m "Initial commit: CSCI 341 Assignment 3 - Caregiver Platform"
```

## Files Included in Git

The following files will be tracked:
- ✅ All Python files (`app.py`, `main.py`, `load_db.py`)
- ✅ All SQL files (`schema.sql`, `sample_data.sql`, `database.sql`)
- ✅ All HTML templates (`templates/` folder)
- ✅ Configuration files (`requirements.txt`, `Procfile`, `runtime.txt`)
- ✅ Documentation (all `.md` files)
- ✅ Test scripts (`test_system.sh`)

## Files Excluded (via .gitignore)

The following will NOT be tracked:
- ❌ `venv/` - Virtual environment
- ❌ `__pycache__/` - Python cache
- ❌ `.env` - Environment variables (sensitive)
- ❌ `*.log` - Log files
- ❌ `.DS_Store` - macOS system files
- ❌ IDE configuration files

## Connect to GitHub

### Option 1: Create New Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click **New repository**
3. Name: `caregiver-platform` (or your choice)
4. **Don't** initialize with README
5. Click **Create repository**

### Option 2: Connect Existing Repository

```bash
# Add remote (replace with your GitHub URL)
git remote add origin https://github.com/yourusername/caregiver-platform.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Recommended Git Workflow

```bash
# Check status
git status

# Add specific files
git add app.py main.py

# Or add all changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push to remote
git push origin main
```

## Important: Don't Commit Sensitive Data

**Never commit:**
- Database passwords
- API keys
- `.env` files
- Personal credentials

**Use environment variables instead:**
- Set in hosting platform
- Use `.env` file locally (already in .gitignore)

## For Deployment

If deploying to Render/Railway/Heroku:
- They can connect directly to your GitHub repo
- Automatic deployments on push
- Environment variables set in dashboard

## Quick Commands

```bash
# Initialize and first commit
git init
git add .
git commit -m "Initial commit"

# Connect to GitHub
git remote add origin <your-repo-url>
git push -u origin main

# Daily workflow
git add .
git commit -m "Update description"
git push
```

