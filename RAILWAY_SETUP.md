# Railway PostgreSQL Setup Instructions

## ✅ Configuration Complete!

Your Django project is now configured to use **ONLY** Railway PostgreSQL database with no local fallback.

## Database Configuration

The `settings.py` file has been updated with:

```python
# Parse DATABASE_URL and add connection parameters
_db_config = dj_database_url.parse(config("DATABASE_URL"))
_db_config.update({
    'CONN_MAX_AGE': 600,
    'CONN_HEALTH_CHECKS': True,
    'OPTIONS': {
        'sslmode': 'require',  # Railway requires SSL
    }
})

DATABASES = {
    "default": _db_config
}
```

## Environment Variables Required

### For Local Development:
Create a `.env` file in your project root with:

```bash
# Required - Railway Database URL
DATABASE_URL=postgresql://postgres:MLZrPOXfglZnqTgfMSWnuVFjEfzabICa@hopper.proxy.rlwy.net:27806/postgres

# Optional - Django settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### For Railway Production:
Set these environment variables in Railway dashboard:
- `DATABASE_URL` (automatically provided by Railway PostgreSQL service)
- `SECRET_KEY` (generate a secure key)
- `DEBUG=False`
- `ALLOWED_HOSTS=your-domain.com`

## Testing the Configuration

### Method 1: Use the test script
```bash
python test_db_connection.py
```

### Method 2: Django shell
```bash
# Set environment variable (Windows PowerShell)
$env:DATABASE_URL="postgresql://postgres:MLZrPOXfglZnqTgfMSWnuVFjEfzabICa@hopper.proxy.rlwy.net:27806/postgres"

# Test configuration
python manage.py shell -c "from django.conf import settings; print(settings.DATABASES['default'])"

# Check database connection
python manage.py check --database default
```

### Method 3: Test migrations
```bash
# Set environment variable first
$env:DATABASE_URL="postgresql://postgres:MLZrPOXfglZnqTgfMSWnuVFjEfzabICa@hopper.proxy.rlwy.net:27806/postgres"

# Run migrations
python manage.py migrate
```

## Key Changes Made

1. ✅ Removed any fallback to localhost or default sqlite/postgres configs
2. ✅ Configured DATABASES to ONLY use Railway's DATABASE_URL environment variable
3. ✅ Used `dj_database_url.parse()` with proper connection parameters
4. ✅ Added SSL requirement for Railway PostgreSQL
5. ✅ Added connection pooling with `CONN_MAX_AGE=600`
6. ✅ Added connection health checks

## Dependencies

Make sure these packages are installed:
- `dj-database-url==3.0.1`
- `python-decouple==3.8`
- `psycopg2-binary==2.9.9`

## Security Notes

- The DATABASE_URL contains sensitive credentials
- Never commit `.env` files to version control
- Use Railway's environment variables in production
- SSL is required for Railway PostgreSQL connections

## Troubleshooting

If you get connection errors:
1. Verify the DATABASE_URL environment variable is set
2. Check that Railway PostgreSQL service is running
3. Ensure your Railway project has the PostgreSQL plugin installed
4. Verify the connection string is correct (host, port, credentials)

## Next Steps

1. Create your `.env` file with the DATABASE_URL
2. Run `python test_db_connection.py` to verify connection
3. Run `python manage.py migrate` to set up database tables
4. Deploy to Railway with proper environment variables
