import os
import time
from typing import List
from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel, format_bytes


def scan_large_files(min_size_mb: int = 100) -> List[CleanableItem]:
    """Scan user folders (Downloads, Documents, Desktop) for files larger than min_size_mb."""
    home = os.path.expanduser("~")
    search_dirs = [
        os.path.join(home, "Downloads"),
        os.path.join(home, "Documents"),
        os.path.join(home, "Desktop"),
    ]

    min_size_bytes = min_size_mb * 1024 * 1024
    items: List[CleanableItem] = []

    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        try:
            for root, dirs, files in os.walk(sdir):
                # Don't descend into hidden directories or git repos
                dirs[:] = [d for d in dirs if not d.startswith(".") and d != "node_modules"]
                
                for f in files:
                    if f.startswith("."):
                        continue
                    full_path = os.path.join(root, f)
                    try:
                        stat = os.stat(full_path)
                        if stat.st_size >= min_size_bytes:
                            mtime = time.strftime("%Y-%m-%d", time.localtime(stat.st_mtime))
                            rel_folder = os.path.basename(root)
                            
                            is_compressible = f.endswith((".sql", ".log", ".txt", ".csv", ".json", ".tar"))
                            
                            desc = f"Folder: {rel_folder} | Modified: {mtime}"
                            if is_compressible:
                                desc += " | Gzip compressible (~80% saving)"

                            items.append(
                                CleanableItem(
                                    id=f"large_file_{abs(hash(full_path))}",
                                    title=f,
                                    description=desc,
                                    path=full_path,
                                    category=CleanableCategory.LARGE_FILES,
                                    risk=RiskLevel.REVIEW,
                                    size_bytes=stat.st_size,
                                    selected=False,
                                    details={"compressible": is_compressible, "mtime": mtime}
                                )
                            )
                    except (OSError, PermissionError):
                        continue
        except (OSError, PermissionError):
            continue

    items.sort(key=lambda x: x.size_bytes, reverse=True)
    return items
