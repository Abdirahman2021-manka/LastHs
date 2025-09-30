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

# Run the application
CMD python manage.py collectstatic --noinput && \
    python manage.py migrate --noinput && \
    gunicorn hasilinvest.wsgi:application --bind 0.0.0.0:$PORT