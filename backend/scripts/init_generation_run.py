import sys
import os
import json
import logging
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.config.app_config import settings
from src.utils.staging_manager import StagingManager

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def init_run():
    """
    Initializes a new generation run by auditing existing content
    and setting up the staging directory.
    """
    # Create staging manager with current run ID
    manager = StagingManager()

    logger.info(f"Initializing Generation Run: {manager.run_id}")
    logger.info(f"Staging Directory: {manager.run_dir}")

    # 1. Perform Audit of existing production content
    logger.info("Auditing production content...")
    audit = manager.audit_production_content()
    logger.info(f"Audit complete. Tracked {len(audit['files'])} JSON files.")

    # 2. Create Initial Run Report
    report = f"""# Generation Run Report: {manager.run_id}
- **Timestamp:** {datetime.utcnow().isoformat()}
- **Staging Area:** `{manager.run_dir}`
- **Source Root:** `{settings.MASTER_CONTENT_ROOT}`
- **Production Audit:** `{os.path.join(manager.run_dir, "PRODUCTION_AUDIT_PRE_GEN.json")}`

## Initial State
- **Total Production Files:** {len(audit['files'])}
- **Run Status:** INITIALIZED

## Safety Rules Applied
1. All generated content written to staging area only.
2. Production content untouched.
3. Every file mapped to source.
4. Validation required before integration.
"""

    with open(os.path.join(manager.run_dir, "GENERATION_REPORT.md"), 'w', encoding='utf-8') as f:
        report_path = f.write(report)

    logger.info(f"Run initialized successfully. Staging area ready at {manager.run_dir}")

if __name__ == "__main__":
    init_run()
