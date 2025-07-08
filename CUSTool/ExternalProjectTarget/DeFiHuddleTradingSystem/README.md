# DeFi Huddle Trading System

## Overview
A cross-platform, automated trading system for retail investors, supporting both backtesting and live trading with Interactive Brokers. Features user-friendly configuration, guided setup, audit logging, AI optimization, and SQLite persistence.

## Features
- BackTesting and Live trading modes
- Interactive Brokers API integration (TWS, Client Portal)
- Backtrader for backtesting
- SQLite for persistence
- AI optimizer (OpenAI API)
- Unified audit logging
- Persistent watchlist (Google Drive sync planned)
- User-friendly CLI wizard for onboarding

## Setup Instructions
1. Install Python 3.11+
2. Clone this repository
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python main.py`

## Usage
- On first launch, follow the CLI wizard to configure your account and preferences.
- Select BackTesting or Live mode as needed.

## Troubleshooting
- Check the audit log at `~/.defihuddle_audit.log` for errors.
- Ensure your Interactive Brokers credentials are correct.
- For support, see the documentation in `/docs`.

## Running Tests
- All tests are environment-agnostic. To run all tests:

  ```sh
  python -m unittest discover -s DeFiHuddleTradingSystem/tests
  ```
- The test suite automatically ensures the `src` directory is on `sys.path` for all test runs.

## Integration Testing with Interactive Brokers (IBKR)

To run integration tests or live trading, you must have TWS or IB Gateway running and accessible. Set up your broker config as follows:

```
"broker": {
    "type": "TWS",           # or "IBG" for IB Gateway
    "host": "127.0.0.1",      # TWS/IBG host
    "port": 7497,               # TWS default port (7497 for paper, 7496 for live)
    "clientId": 1               # Any unique integer
}
```

Set the environment variable `TEST_MODE=integration` to enable real API calls:

- On Windows PowerShell:
  ```powershell
  $env:TEST_MODE='integration'; python -m unittest discover -s DeFiHuddleTradingSystem/tests
  ```
- On Linux/macOS:
  ```bash
  TEST_MODE=integration python -m unittest discover -s DeFiHuddleTradingSystem/tests
  ```

If TWS/IB Gateway is not running or the config is incorrect, integration tests will fail with a clear error message.

## Quickstart Example
1. Launch the CLI wizard: `python main.py`
2. Follow prompts to configure your account and preferences.
3. Select BackTesting or Live mode.
4. Review audit logs at `~/.defihuddle_audit.log` for activity and errors.

## Glossary of Key Terms
- **BackTesting**: Simulated trading using historical data.
- **Live Trading**: Real trades with Interactive Brokers.
- **Audit Log**: Centralized log of all trading activity and errors.
- **Watchlist**: Persistent list of symbols to monitor/trade.
- **Configurable**: Any setting or logic the user can change via UI or config file.

## Configuration & Customization
- All major settings are accessible via the CLI wizard or config files in `/config`.
- See `/docs/Project_Requirements.md` for a list of all configurable items.

## Error Handling
- Errors are logged in the audit log and displayed in plain language.
- For troubleshooting, see `/docs/DevelopmentProcessAssumptionsLog.md` and `/docs/Architecture_Document.md`.
