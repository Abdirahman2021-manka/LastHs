@echo off
echo 🚀 Deploying Image Fixes to Production
echo =====================================

echo.
echo 📁 Adding all changes to Git...
git add .

echo.
echo 💾 Committing changes...
git commit -m "Fix image display issues, media serving, and CSRF errors for production"

echo.
echo 🚀 Pushing to Railway...
git push origin main

echo.
echo ✅ Deployment started!
echo.
echo Next steps:
echo 1. Go to Railway dashboard
echo 2. Wait for deployment to complete
echo 3. Run: python manage.py collectstatic --noinput
echo 4. Upload your media files
echo 5. Restart the service
echo.
echo Your images should work after deployment!
pause
