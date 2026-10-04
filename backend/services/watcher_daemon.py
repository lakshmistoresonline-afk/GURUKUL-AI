import os
import sys
import time
import subprocess
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("WatcherDaemon")

REPO_ROOT = r"D:/GURUKUL"
CONTENTS_ROOT = os.path.join(REPO_ROOT, "Contents")

class WatcherDaemon:
    """
    Real-time file system watcher daemon for Gurukul AI.
    Monitors Contents/ for any modifications and triggers incremental processing.
    """
    def __init__(self, poll_interval_seconds: int = 5):
        self.poll_interval = poll_interval_seconds
        self.last_mtime_cache = {}
        self._build_mtime_cache()

    def _build_mtime_cache(self):
        if not os.path.exists(CONTENTS_ROOT):
            return
        for root, dirs, files in os.walk(CONTENTS_ROOT):
            for file in files:
                if file.endswith(".json"):
                    f_abs = os.path.join(root, file)
                    try:
                        self.last_mtime_cache[f_abs] = os.path.getmtime(f_abs)
                    except:
                        pass

    def check_for_updates(self) -> bool:
        updated = False
        for root, dirs, files in os.walk(CONTENTS_ROOT):
            for file in files:
                if file.endswith(".json"):
                    f_abs = os.path.join(root, file)
                    try:
                        mtime = os.path.getmtime(f_abs)
                        if f_abs not in self.last_mtime_cache or self.last_mtime_cache[f_abs] < mtime:
                            logger.info(f"Detected change in source file: {os.path.relpath(f_abs, REPO_ROOT)}")
                            self.last_mtime_cache[f_abs] = mtime
                            updated = True
                    except:
                        pass
        return updated

    def trigger_reprocessing(self):
        logger.info("Triggering autonomous reprocessing pipeline...")
        try:
            subprocess.run([sys.executable, os.path.join(REPO_ROOT, "backend", "scripts", "generate_processed_content_strict_1to1.py")], check=True)
            logger.info("Autonomous reprocessing completed successfully.")
        except Exception as e:
            logger.error(f"Error during autonomous reprocessing: {e}")

    def run_once(self) -> bool:
        if self.check_for_updates():
            self.trigger_reprocessing()
            return True
        return False

if __name__ == "__main__":
    daemon = WatcherDaemon()
    logger.info("WatcherDaemon initialized in read-only monitoring mode.")
    # Run once for check
    daemon.run_once()
