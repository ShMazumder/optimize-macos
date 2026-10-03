import os
from typing import Optional


def get_path_size(path: str) -> int:
    """Recursively calculate the size of a file or directory in bytes."""
    expanded = os.path.expanduser(path)
    if not os.path.exists(expanded):
        return 0

    if os.path.islink(expanded):
        return 0

    if os.path.isfile(expanded):
        try:
            return os.path.getsize(expanded)
        except OSError:
            return 0

    total = 0
    try:
        with os.scandir(expanded) as it:
            for entry in it:
                try:
                    if entry.is_symlink():
                        continue
                    if entry.is_file():
                        total += entry.stat().st_size
                    elif entry.is_dir():
                        total += get_path_size(entry.path)
                except (OSError, PermissionError):
                    continue
    except (OSError, PermissionError):
        pass
    return total
