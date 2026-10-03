import os
import shutil
import subprocess
import re
from mac_opt.models import DiskStats


def get_disk_stats() -> DiskStats:
    """Fetch accurate APFS disk statistics."""
    try:
        # First try diskutil for container free space (APFS aware)
        res = subprocess.run(
            ["diskutil", "info", "/"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if res.returncode == 0:
            total_bytes = 0
            free_bytes = 0
            
            for line in res.stdout.splitlines():
                if "Container Total Space:" in line or "Total Space:" in line:
                    match = re.search(r"\((\d+)\s+Bytes\)", line)
                    if match:
                        total_bytes = int(match.group(1))
                elif "Container Free Space:" in line or "Free Space:" in line or "Volume Available Space:" in line:
                    match = re.search(r"\((\d+)\s+Bytes\)", line)
                    if match:
                        free_bytes = int(match.group(1))
            
            if total_bytes > 0 and free_bytes > 0:
                used_bytes = max(0, total_bytes - free_bytes)
                return DiskStats(
                    total_bytes=total_bytes,
                    free_bytes=free_bytes,
                    used_bytes=used_bytes,
                    container_name="Macintosh HD"
                )
    except Exception:
        pass

    # Fallback to standard shutil.disk_usage
    total, used, free = shutil.disk_usage("/")
    return DiskStats(
        total_bytes=total,
        free_bytes=free,
        used_bytes=used,
        container_name="Macintosh HD"
    )
