from __future__ import annotations

from datetime import datetime, timezone
import uuid # unique identifier

def generate_run_id() -> str:
    """
    Generate a unique, sortable run identifier.

    Format:
        YYYYMMDD_HHMMSS_<8-char-uuid>

    Example:
        20251224-145233_a1b2c3d4
    """

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    uid = uuid.uuid4().hex[:8]

    return f"{timestamp}_{uid}"