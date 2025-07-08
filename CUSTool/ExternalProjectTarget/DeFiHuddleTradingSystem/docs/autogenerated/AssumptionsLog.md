# Assumptions Log

## 2025-07-04
- Using ib_insync for Interactive Brokers integration (TWS/Client Portal). Credentials are username/password for MVP; OAuth and advanced flows will be added later.
- OpenAI API key and settings will be provided in config['ai_optimizer'].
- SQLite DB and config files will be stored in the user's home directory for simplicity and cross-platform compatibility.
- Google Drive sync for watchlist will be implemented after core trading logic is complete.
- sqlite3 is part of the Python standard library and should not be included in requirements.txt. It has been removed from the dependency list.
