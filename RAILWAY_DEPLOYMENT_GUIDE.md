# 🚀 Railway Deployment Guide - Fix Image Issues

## Problem
Your production website (hasilinvest.ca) is showing broken images because the production server doesn't have the latest fixes.

## Solution
Deploy the image fixes to your Railway production server.

## Steps to Fix

### 1. 📁 Commit Your Changes
```bash
git add .
git commit -m "Fix image display issues and media serving"
git push origin main
```

### 2. 🚀 Deploy to Railway
Railway should automatically deploy when you push to main. If not:
- Go to your Railway dashboard
- Click "Deploy" or "Redeploy"

### 3. 🔧 Run Commands on Railway
After deployment, run these commands in Railway's console:

```bash
python manage.py collectstatic --noinput
python manage.py migrate
```

### 4. 📤 Upload Media Files
You need to upload your media files to Railway:

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link your project
railway login
railway link

# Upload media files
railway run --service web python manage.py shell
# Then in the shell:
from django.core.files.storage import default_storage
# Upload your files programmatically
```

**Option B: Manual Upload**
- Go to Railway dashboard
- Navigate to your project
- Go to "Variables" tab
- Add a new variable for file uploads
- Or use Railway's file upload feature

### 5. 🔄 Restart Service
- Go to Railway dashboard
- Click "Restart" on your service

## What We Fixed

1. **Media File Serving**: Added proper URL routing for media files
2. **Image Error Handling**: Added fallback images when images fail to load
3. **Static File Collection**: Fixed static file serving
4. **Database Connection**: Added error handling for database issues

## Test After Deployment

1. Visit your website: https://hasilinvest.ca
2. Check if blog post images load correctly
3. Check if CSS styles are applied
4. Check if the logo image loads

## If Images Still Don't Work

1. Check Railway logs for errors
2. Verify media files are uploaded to `/media` directory
3. Check if `MEDIA_URL` and `MEDIA_ROOT` are set correctly
4. Ensure the custom media serving view is working

## Quick Fix Commands

If you have Railway CLI installed:
```bash
railway login
railway link
railway run python manage.py collectstatic --noinput
railway run python manage.py migrate
railway up
```

## Need Help?

If you're still having issues:
1. Check Railway logs in the dashboard
2. Verify your environment variables
3. Make sure all files are committed and pushed
4. Check if the database connection is working
