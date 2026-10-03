import os
import shutil
import subprocess
from typing import List, Tuple
from mac_opt.models import CleanableItem


def clean_items(items: List[CleanableItem], dry_run: bool = False) -> Tuple[int, List[str]]:
    """
    Executes cleaning for selected items.
    Returns: (total_bytes_freed, list_of_log_messages)
    """
    total_freed = 0
    logs: List[str] = []

    for item in items:
        if not item.selected:
            continue

        if dry_run:
            total_freed += item.size_bytes
            logs.append(f"[DRY-RUN] Would clean '{item.title}' ({item.size_human})")
            continue

        # Real cleaning
        freed = 0
        try:
            if item.custom_action == "simctl_runtime":
                runtime_id = item.details.get("runtime_id")
                if runtime_id:
                    res = subprocess.run(
                        ["xcrun", "simctl", "runtime", "delete", runtime_id],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    if res.returncode == 0:
                        freed = item.size_bytes
                        logs.append(f"Deleted simulator runtime: {item.title}")
                    else:
                        logs.append(f"Failed to delete runtime: {res.stderr.strip()}")
            elif item.custom_action == "simctl_erase":
                subprocess.run(["xcrun", "simctl", "delete", "unavailable"], capture_output=True, timeout=15)
                subprocess.run(["xcrun", "simctl", "erase", "all"], capture_output=True, timeout=30)
                freed = item.size_bytes
                logs.append("Erased all iOS simulator devices and caches")
            elif item.custom_action == "uv":
                subprocess.run(["uv", "cache", "clean"], capture_output=True, timeout=30)
                if os.path.exists(item.path):
                    shutil.rmtree(item.path, ignore_errors=True)
                freed = item.size_bytes
                logs.append("Purged Python UV package cache")
            elif item.custom_action == "npm":
                subprocess.run(["npm", "cache", "clean", "--force"], capture_output=True, timeout=30)
                if os.path.exists(item.path):
                    shutil.rmtree(item.path, ignore_errors=True)
                freed = item.size_bytes
                logs.append("Purged Node NPM cache")
            elif item.custom_action == "brew":
                subprocess.run(["brew", "cleanup", "-s"], capture_output=True, timeout=60)
                freed = item.size_bytes
                logs.append("Cleaned Homebrew download bottles")
            elif item.custom_action == "antigravity_scratch":
                brain_root = item.path
                if os.path.exists(brain_root):
                    # Delete scratch dirs and png images
                    for entry in os.scandir(brain_root):
                        if entry.is_dir():
                            s_path = os.path.join(entry.path, "scratch")
                            if os.path.exists(s_path):
                                shutil.rmtree(s_path, ignore_errors=True)
                    freed = item.size_bytes
                    logs.append("Cleaned Antigravity scratch scripts and test directories")
            else:
                # Standard directory/file removal
                p = item.path
                if os.path.exists(p):
                    if os.path.isdir(p):
                        # Empty contents of directory rather than deleting the root directory for special folders like .Trash
                        if os.path.basename(p) in [".Trash", "Google", "Logs"]:
                            for child in os.scandir(p):
                                try:
                                    if child.is_dir():
                                        shutil.rmtree(child.path, ignore_errors=True)
                                    else:
                                        os.remove(child.path)
                                except Exception:
                                    pass
                        else:
                            shutil.rmtree(p, ignore_errors=True)
                    else:
                        os.remove(p)
                    freed = item.size_bytes
                    logs.append(f"Cleaned {item.title} ({item.size_human})")
                else:
                    logs.append(f"Already clean: {item.title}")

        except Exception as e:
            logs.append(f"Error cleaning {item.title}: {str(e)}")

        total_freed += freed

    return total_freed, logs
