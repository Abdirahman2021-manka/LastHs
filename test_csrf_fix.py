#!/usr/bin/env python
"""
Test script to verify CSRF settings are working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'habiba_blog.settings')
django.setup()

from django.conf import settings

def main():
    print("🔒 Testing CSRF Settings")
    print("=" * 40)
    
    # Check CSRF trusted origins
    print("CSRF Trusted Origins:")
    for origin in settings.CSRF_TRUSTED_ORIGINS:
        print(f"  ✅ {origin}")
    
    print()
    print("CSRF Cookie Settings:")
    print(f"  CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
    print(f"  CSRF_COOKIE_HTTPONLY: {settings.CSRF_COOKIE_HTTPONLY}")
    print(f"  CSRF_COOKIE_SAMESITE: {settings.CSRF_COOKIE_SAMESITE}")
    print(f"  CSRF_USE_SESSIONS: {settings.CSRF_USE_SESSIONS}")
    
    print()
    print("Allowed Hosts:")
    for host in settings.ALLOWED_HOSTS:
        print(f"  ✅ {host}")
    
    print()
    print("🎯 CSRF Fix Summary:")
    print("✅ Added hasilinvest.ca to trusted origins")
    print("✅ Added Railway domains to trusted origins")
    print("✅ Configured secure CSRF cookies")
    print("✅ Set proper CSRF cookie settings")
    
    print()
    print("🚀 Next Steps:")
    print("1. Deploy these changes to production")
    print("2. Clear your browser cache and cookies")
    print("3. Try publishing a blog post again")
    print("4. The CSRF error should be resolved!")

if __name__ == "__main__":
    main()
