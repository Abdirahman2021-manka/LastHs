#!/usr/bin/env python
import os
import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"ERROR: Command failed with code {result.returncode}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return False
    else:
        print(f"SUCCESS: {cmd}")
        if result.stdout:
            print(f"OUTPUT: {result.stdout}")
    return True

if __name__ == "__main__":
    print("=== ENTRYPOINT STARTING ===")
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Environment variables: PORT={os.environ.get('PORT', '8000')}")
    
    # Check if manage.py exists
    if not os.path.exists('manage.py'):
        print("ERROR: manage.py not found!")
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate --noinput"):
        print("ERROR: Migrations failed!")
        sys.exit(1)
    print("=== MIGRATIONS COMPLETE ===")
    
    # Collect static files
    if not run_command("python manage.py collectstatic --noinput --clear"):
        print("ERROR: Collectstatic failed!")
        sys.exit(1)
    print("=== COLLECTSTATIC COMPLETE ===")
    
    # Test Django app
    print("=== TESTING DJANGO APP ===")
    if not run_command("python manage.py check --deploy"):
        print("WARNING: Django check failed, but continuing...")
    
    port = os.environ.get('PORT', '8000')
    print(f"=== STARTING GUNICORN ON PORT {port} ===")
    
    # Start Gunicorn
    try:
        os.execvp("gunicorn", [
            "gunicorn",
            "habiba_blog.wsgi:application",
            "--bind", f"0.0.0.0:{port}",
            "--workers", "3",
            "--timeout", "120",
            "--log-level", "info",
            "--access-logfile", "-",
            "--error-logfile", "-",
            "--preload"
        ])
    except Exception as e:
        print(f"ERROR: Failed to start Gunicorn: {e}")
        sys.exit(1)