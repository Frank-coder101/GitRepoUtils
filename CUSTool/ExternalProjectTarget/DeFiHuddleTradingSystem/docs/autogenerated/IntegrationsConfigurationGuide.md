# Integrations Configuration Guide

This guide provides step-by-step instructions for configuring and authenticating integrations required for the DeFi Huddle Trading System.

## 1. Interactive Brokers (IBKR) API

### Prerequisites
- Install the IBKR TWS or IB Gateway software.
- Ensure the API is enabled in the IBKR software settings.

### Configuration
- File: `config/ibkr_config.json`
- Required Fields:
  ```json
  {
    "host": "127.0.0.1",
    "port": 7497,
    "client_id": 123
  }
  ```
- Environment Variable: `IBKR_API_KEY`

### Troubleshooting
- Ensure TWS or IB Gateway is running and accessible.
- Verify API settings in the IBKR software.
- Check logs for detailed error messages in `~/.defihuddle_audit.log`.
- Use the `test_broker_manager.py` script to validate connectivity.

## 2. Google Drive Watchlist Sync

### Prerequisites
- Install the Google Drive API Python client library.
- Obtain OAuth 2.0 credentials from the Google Cloud Console.

### Configuration
- File: `config/gdrive_config.json`
- Required Fields:
  ```json
  {
    "client_id": "your-client-id",
    "client_secret": "your-client-secret",
    "refresh_token": "your-refresh-token"
  }
  ```
- Environment Variable: `GDRIVE_API_KEY`

### Verification
- Run the `tests/test_watchlist_manager.py` test suite.
- Ensure watchlist synchronization works as expected.

## 3. OpenAI Integration

### Prerequisites
- Install the OpenAI Python client library.
- Obtain an API key from the OpenAI dashboard.

### Configuration
- File: `config/openai_config.json`
- Required Fields:
  ```json
  {
    "api_key": "your-api-key"
  }
  ```
- Environment Variable: `OPENAI_API_KEY`

### Verification
- Run the `tests/test_ai_optimizer.py` test suite.
- Ensure AI optimization functions correctly.

## 4. Database Integration

### Prerequisites
- Install the PostgreSQL database server.
- Install the `psycopg2` Python library.

### Configuration
- File: `config/db_config.json`
- Required Fields:
  ```json
  {
    "host": "localhost",
    "port": 5432,
    "database": "trading_system",
    "user": "your-username",
    "password": "your-password"
  }
  ```
- Environment Variable: `DB_CONNECTION_STRING`

### Verification
- Run the `tests/test_persistence.py` test suite.
- Ensure database operations are functional.

## Troubleshooting
- Check log files in the `logs/` directory for error details.
- Verify that all required services are running and accessible.
- Consult the official documentation for each integration for additional support.
