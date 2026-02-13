from datetime import datetime, timezone
from uuid import uuid4


def run_id() -> str:
    """
    Generate a lexicographically sortable and globally unique run ID.

    Format:
        YYYYMMDDTHHMMSSZ_<12-hex>
    
    Example:
        20260213T094912Z_7f3a9c2b5d3e
    """
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    nonce = uuid4().hex[:12] # a number used once (nonce)
    return f"{ts}_{nonce}"