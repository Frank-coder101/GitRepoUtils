import os
import json
import csv
from datetime import datetime
from src.core.logger import Logger

TRADE_JOURNAL_JSON = os.path.expanduser("~/.defihuddle_trade_journal.json")
TRADE_JOURNAL_CSV = os.path.expanduser("~/.defihuddle_trade_journal.csv")

class TradeJournal:
    @staticmethod
    def log_trade(entry):
        # Ensure required fields
        entry.setdefault('entry_timestamp', datetime.utcnow().isoformat() + 'Z')
        entry.setdefault('exit_timestamp', None)
        entry.setdefault('entry_score', None)
        entry.setdefault('signal_rationale', None)
        entry.setdefault('exit_reason', None)
        entry.setdefault('screenshots', [])
        entry.setdefault('performance', {})
        # Append to JSON
        if not os.path.exists(TRADE_JOURNAL_JSON):
            with open(TRADE_JOURNAL_JSON, 'w') as f:
                json.dump([entry], f, indent=4)
        else:
            with open(TRADE_JOURNAL_JSON, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=4)
        # Append to CSV
        TradeJournal._append_csv(entry)
        Logger.info(f"Trade journal entry logged for symbol: {entry.get('symbol')}")

    @staticmethod
    def _append_csv(entry):
        fieldnames = [
            'symbol', 'entry_timestamp', 'exit_timestamp', 'entry_score', 'signal_rationale',
            'exit_reason', 'screenshots', 'pnl', 'drawdown', 'slippage'
        ]
        file_exists = os.path.exists(TRADE_JOURNAL_CSV)
        with open(TRADE_JOURNAL_CSV, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            row = {
                'symbol': entry.get('symbol'),
                'entry_timestamp': entry.get('entry_timestamp'),
                'exit_timestamp': entry.get('exit_timestamp'),
                'entry_score': entry.get('entry_score'),
                'signal_rationale': entry.get('signal_rationale'),
                'exit_reason': entry.get('exit_reason'),
                'screenshots': ';'.join(entry.get('screenshots', [])),
                'pnl': entry.get('performance', {}).get('pnl'),
                'drawdown': entry.get('performance', {}).get('drawdown'),
                'slippage': entry.get('performance', {}).get('slippage'),
            }
            writer.writerow(row)
