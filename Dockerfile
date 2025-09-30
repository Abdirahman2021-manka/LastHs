FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Don't collect static during build - do it at runtime when env vars are available
CMD echo "Starting application..." && \
    python manage.py migrate --noinput && \
    echo "Migrations complete" && \
    python manage.py collectstatic --noinput --clear && \
    echo "Static files collected" && \
    echo "Starting Gunicorn..." && \
    gunicorn habiba_blog.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info