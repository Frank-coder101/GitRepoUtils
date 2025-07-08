# Assumption (2025-07-04): Google Drive sync is stubbed for now. Real implementation will use Google Drive API and OAuth2.
from src.core.logger import Logger
import os

TEST_MODE = os.environ.get('TEST_MODE', 'unit').lower()

class GDriveWatchlistSync:
    def __init__(self, config):
        self.config = config

    def sync(self, watchlist):
        if TEST_MODE == 'integration':
            Logger.info("[INTEGRATION] Syncing watchlist with Google Drive (real implementation required)")
            print("DEBUG: About to raise RuntimeError in integration mode!")
            raise RuntimeError("[INTEGRATION] Forced failure for test validation.")
            # if not self.config.get('gdrive_access_token'):
            #     raise RuntimeError("[INTEGRATION] Google Drive credentials not provided.")
            # TODO: Implement real Google Drive sync here
            # return watchlist
        else:
            Logger.info("[UNIT] Stub: Syncing watchlist with Google Drive (not implemented)")
            return watchlist
