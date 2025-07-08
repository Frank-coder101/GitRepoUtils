# IBKR IT Assets Report

The below is a report of all applications, API, systems and components that may fulfill requirements of the project.
It is important to analyze this content before attempting to provide an architecture, design or implementation of the system.

# 1. Integration Capabilities
1.1 Client Portal (Web) API: Modern RESTful API with OAuth and WebSocket support for trading, positions, balances, and real-time updates
1.2 Trader Workstation (TWS) API: Desktop-based API with support for Java, Python, C++, C#, Excel; enables real-time data, order entry, and account access
1.3 FIX API: High-performance FIX protocol for institutional traders to place orders via extranet or direct connection (no market data)
1.4 Market Data Feeds: Subscribe to real-time and historical data via API (WebSocket/REST) – requires exchange-specific permissions

# 2. Technology Stack
2.1 Python 3.11 (Strategy & Control Layer)
2.2 ib_insync, TWS (Live Data + Orders)
2.3 Backtrader (Backtest Engine)
2.4 SQLite (Persistence: config, logs, alerts, watchlists, risk mgmt, market data, backtest, training datasets)
2.5 OpenAI API (AI Optimizer)
2.6 Platform Abstraction Layer (Windows, macOS, Linux)
2.7 Google Drive API (Watchlist sync)
2.8 NewsAPI/Yahoo Finance RSS (News events)
2.9 CLI Wizard (Initial config, onboarding)
2.10 Electron (GUI)

# 3. Application Domain Architecture
## 3.1 Component Model
| Artifact Number | Component Name                | Description |
|----------------|------------------------------|-------------|
| APP-1          | User Interface (CLI Wizard)  | Terminal-based configuration wizard for onboarding, settings, and mode selection |
| APP-2          | Funds Input Component         | UI and logic for user to input available funds |
| APP-3          | Broker Connection Manager     | Handles authentication and connection to broker APIs |
| APP-4          | Execution Cycle Controller    | Manages BackTesting and Live modes, schedules cycles |
| APP-5          | Live Mode Confirmation Dialog | Prompts user for explicit confirmation before live trading |
| APP-6          | Config UI                    | Grouped, expandable/collapsible settings interface |
| APP-7          | Installer/Setup Engine        | Automates environment setup and initial config |
| APP-8          | Mode Selection Menu           | Menu for BackTesting/Live mode selection |
| APP-9          | Feature Abstraction Layer     | Wraps advanced features behind simple options |
| APP-10         | Error Handler                 | User-facing error handler with actionable suggestions |
| APP-11         | Order Management Engine       | Handles order placement, scale in/out, bracket order adjustments |
| APP-12         | Backtest Engine               | Simulates regime transitions, stop-loss/TP logic, multi-scenario runs |
| APP-13         | AI Optimizer Engine           | Handles auto-tuning, learning cycles, enhancement activation |
| APP-14         | Analysis Engine               | Implements all technical analysis and scoring |
| APP-15         | Cycle Manager                 | Manages and schedules all execution cycles |
| APP-16         | Options Module                | Handles options logic (deferred) |
| APP-17         | Crypto Module                 | Handles crypto logic (deferred) |
| APP-18         | Futures Module                | Handles futures logic (deferred) |
| APP-19         | Risk Engine                   | Calculates and enforces risk metrics, margin monitoring, R:R enforcement |
| APP-20         | Price Slope Calculator        | Calculates price slope for order adjustment |
| APP-21         | Trailing Stop Engine          | Manages trailing stop logic |
| APP-22         | Documentation Suite           | Install guide, config help, error list, trade logic docs, glossary |
| APP-23         | Remote Access Module          | Web/mobile interface for portfolio viewing (read-only) |
| APP-24         | Crash Recovery Engine         | Persists and restores runtime state |
| APP-25         | Emergency Stop Handler        | Handles emergency stop and resume |
| APP-26         | Symbol Lifecycle Manager      | Manages symbol activation/deactivation |
| APP-27         | Market Hours Engine           | Validates market open/close and edge cases |
| APP-28         | Broker Retry Handler          | Handles broker API retries and errors |
| APP-29         | Broker Capability Validator   | Checks broker account capabilities |

## 3.2 Data Domain Model
| Artifact Number | Data Component Name           | Description |
|----------------|------------------------------|-------------|
| DATA-1         | Localization Module           | Handles region-specific settings and data |
| DATA-2         | Market Data Adapter           | Abstracts and manages all market data sources |
| DATA-3         | FEE Data Fetcher              | Fetches and manages fee data from broker |
| DATA-4         | Watchlist Manager             | Manages persistent watchlist and Google Drive sync |
| DATA-5         | Audit Log Engine              | Centralized logging for orders, rejections, confirmations |
| DATA-6         | Config Store                  | Centralized SQLite config with inline help |
| DATA-7         | Backtest Data Loader          | Loads and manages backtest datasets |
| DATA-8         | KPI Logger                    | Logs KPIs for each strategy |
| DATA-9         | Training Log Engine           | Logs for ML/AI training and auto-tuning |
| DATA-10        | Temp Symbol Table             | Manages temporary symbol table for opportunity selection |
| DATA-11        | Error Log Engine              | Logs errors with unique IDs and manages log rotation |
| DATA-12        | Trade Journal Engine          | Logs trade journal entries for debugging |

## 3.3 Technology Domain Model
| Artifact Number | Technology Component Name     | Description |
|----------------|------------------------------|-------------|
| TECH-1         | Platform Abstraction Layer    | Ensures compatibility and OS-specific handling |
| TECH-2         | SQLite Database               | Unified persistence for config, logs, data |
| TECH-3         | Google Drive API Integration  | Watchlist sync |
| TECH-4         | NewsAPI/Yahoo RSS Integration | News event ingestion |
| TECH-5         | OpenAI API Integration        | AI optimizer and auto-tuning |
| TECH-6         | Scheduler                     | In-code (sleep & callbacks) |

# 4. Sequence Diagrams
## 4.1 User Onboarding and Configuration
1. User launches CLI Wizard
2. CLI Wizard prompts for funds, broker connection, and settings
3. Config Store saves user input
4. Broker Connection Manager authenticates and validates account
5. Mode Selection Menu presents BackTesting/Live options
6. User selects mode; Execution Cycle Controller starts cycles

## 4.2 BackTesting Cycle
1. Cycle Manager triggers Backtest Engine
2. Backtest Data Loader loads dataset
3. Analysis Engine scores opportunities
4. Order Management Engine simulates trades
5. KPI Logger and Training Log Engine persist results

## 4.3 Live Trading Cycle
1. Cycle Manager triggers Execution Cycle Controller
2. Market Data Adapter fetches live data
3. Analysis Engine scores opportunities
4. Order Management Engine places orders via Broker Connection Manager
5. Audit Log Engine and Trade Journal Engine persist results
6. Risk Engine monitors margin and risk

## 4.4 Emergency Stop
1. User triggers Emergency Stop Handler
2. All open orders are canceled
3. Trading is disabled until user re-enables
4. State is persisted by Crash Recovery Engine

# 5. Entity Relationship Diagram (ERD)
Entities:
- User
- Configuration
- Watchlist
- Portfolio Position
- Order
- Trade Journal
- Audit Log
- Error Log
- Enhancement Log
- Training Log
- Symbol
- Market Data

Relationships:
- User has Configuration
- User has Watchlist
- User has Portfolio Positions
- Portfolio Position has Orders
- Order has Trade Journal
- Order has Audit Log
- Error Log relates to Order, Trade, or System Event
- Enhancement Log and Training Log relate to Configuration and Code
- Symbol relates to Market Data, Watchlist, Portfolio Position

# 6. Component Interaction Matrix
| Component | Interacts With |
|-----------|---------------|
| User Interface (CLI Wizard) | Config Store, Broker Connection Manager, Mode Selection Menu |
| Broker Connection Manager | Broker APIs, Order Management Engine, Risk Engine |
| Execution Cycle Controller | Cycle Manager, Backtest Engine, Order Management Engine, Risk Engine |
| Order Management Engine | Broker Connection Manager, Audit Log Engine, Trade Journal Engine, Trailing Stop Engine |
| Analysis Engine | Market Data Adapter, KPI Logger, Training Log Engine, Risk Engine |
| AI Optimizer Engine | Training Log Engine, Enhancement Log, Config Store |
| Crash Recovery Engine | Config Store, Portfolio Position, Order, Cycle Manager |
| Emergency Stop Handler | Order Management Engine, Crash Recovery Engine |
| Symbol Lifecycle Manager | Watchlist Manager, Market Data Adapter |
| Market Hours Engine | Market Data Adapter, Order Management Engine |
| Broker Retry Handler | Broker Connection Manager, Error Log Engine |
| Broker Capability Validator | Broker Connection Manager, User Interface |

# 7. Numbering and Naming Conventions
- All artifacts are numbered as APP-#, DATA-#, TECH-#
- All requirements are mapped to artifacts in the Requirements Traceability Matrix
- All diagrams and models are referenced by section and artifact number

# 8. Glossary
- See Documentation Suite (APP-22) for glossary and external references

# 9. Documentation
- All architecture artifacts, diagrams, and models are documented in the Documentation Suite (APP-22)
- Requirements Traceability Matrix is maintained in CSV format

# 10. Future/Deferred Modules
- Options Module (APP-16), Crypto Module (APP-17), Futures Module (APP-18), GUI (Tkinter/Electron)

# 11. Appendix
- All diagrams and models are available in the docs/ folder as .png/.svg/.drawio files (to be generated)

# 12. Revision History
- v2.0 (2025-07-04): Enhanced architecture, full domain/component/data/tech models, all artifacts numbered and mapped to requirements, sequence diagrams, ERD, interaction matrix, glossary, and traceability matrix.

# CLARIFICATIONS
The file `Architecture_Document.md` referenced in the prompt does not exist in the workspace. I will use `Interactive Brokers Tech Brief.md` and the Requirements Traceability Matrix as the primary architecture sources.
All required API keys, credentials, and access tokens for Interactive Brokers and Google Drive will be provided by the user during configuration or setup.
The initial implementation will focus on terminal-based (CLI) configuration and UI, as GUI is optional for the first release.
The OpenAI API key for AI optimizer functionality will be provided by the user and stored securely in the configuration.
All deferred features (options, crypto, futures, full remote trading) will be stubbed with clear documentation and not implemented in the first release.
The SQLite database will be used for all persistence needs, including configuration, logs, watchlists, and backtest data.
The application will be developed in Python 3.11, as specified in the tech brief.
The user will have Python, pip, and required system dependencies installed prior to running the installer/setup script.
The application will be structured according to the Requirements Traceability Matrix, with each artifact implemented as a separate module/class.
All error codes and logging formats will follow the conventions outlined in the requirements and architecture documents.

## Code Structure Overview
- `src/` contains all core modules, data adapters, integration, and UI logic.
- Each module maps to an artifact/component in the architecture tables above.
- Tests for each module are in `tests/` and follow the same naming convention.

## Extending the System
- To add new assets, create a new module in `src/` and update the relevant manager/engine.
- To add new strategies, extend the Analysis or Backtest Engine.
- For new integrations (brokers, data), add adapters in `src/integration/` or `src/data/`.

## Testing & CI/CD
- All tests are in `tests/` and can be run with `python -m unittest discover -s tests`.
- CI/CD should run all tests and lint checks on push.

## API Documentation
- Main entry points: `main.py`, CLI wizard, and config files.
- Each module and class is documented with docstrings.
- See `/docs/Project_Requirements.md` for requirement-to-code mapping.
