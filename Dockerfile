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

# Create a startup script
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running migrations..."\n\
python manage.py migrate --noinput\n\
echo "Collecting static files..."\n\
python manage.py collectstatic --noinput || echo "collectstatic failed, continuing..."\n\
echo "Starting gunicorn..."\n\
exec gunicorn hasilinvest.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --log-level debug\n\
' > /app/start.sh && chmod +x /app/start.sh

CMD ["/app/start.sh"]