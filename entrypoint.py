#!/usr/bin/env python
import os
import sys
import subprocess

def run_command(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"Warning: Command failed with code {result.returncode}")
    return result.returncode

if __name__ == "__main__":
    print("=== ENTRYPOINT STARTING ===")
    
    run_command("python manage.py migrate --noinput")
    print("=== MIGRATIONS COMPLETE ===")
    
    run_command("python manage.py collectstatic --noinput --clear")
    print("=== COLLECTSTATIC COMPLETE ===")
    
    port = os.environ.get('PORT', '8000')
    print(f"=== STARTING GUNICORN ON PORT {port} ===")
    
    os.execvp("gunicorn", [
        "gunicorn",
        "habiba_blog.wsgi:application",
        "--bind", f"0.0.0.0:{port}",
        "--workers", "2",
        "--timeout", "120",
        "--log-level", "info"
    ])