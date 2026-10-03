import os
import json
from typing import List
from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel
from mac_opt.utils import get_path_size


def scan_chrome_profiles() -> List[CleanableItem]:
    """Scan Google Chrome profiles from Local State, extracting names, emails, and sizes."""
    home = os.path.expanduser("~")
    chrome_root = os.path.join(home, "Library", "Application Support", "Google", "Chrome")
    local_state_path = os.path.join(chrome_root, "Local State")

    if not os.path.exists(chrome_root) or not os.path.exists(local_state_path):
        return []

    profile_metadata = {}
    try:
        with open(local_state_path, "r", encoding="utf-8", errors="ignore") as f:
            data = json.load(f)
            info_cache = data.get("profile", {}).get("info_cache", {})
            for prof_dir, meta in info_cache.items():
                name = meta.get("name", prof_dir)
                user_name = meta.get("user_name", "")
                profile_metadata[prof_dir] = {
                    "name": name,
                    "email": user_name,
                }
    except Exception:
        pass

    items: List[CleanableItem] = []

    # Check all profile folders
    try:
        for entry in os.scandir(chrome_root):
            if entry.is_dir() and (entry.name == "Default" or entry.name.startswith("Profile ")):
                prof_dir = entry.name
                meta = profile_metadata.get(prof_dir, {})
                display_name = meta.get("name", prof_dir)
                email = meta.get("email", "")

                label = f"{display_name}"
                if email and email != display_name:
                    label += f" ({email})"

                prof_path = entry.path
                size = get_path_size(prof_path)

                items.append(
                    CleanableItem(
                        id=f"chrome_profile_{prof_dir.lower().replace(' ', '_')}",
                        title=f"Chrome: {label}",
                        description=f"Directory: Chrome/{prof_dir}. Contains cookies, web storage, and extensions.",
                        path=prof_path,
                        category=CleanableCategory.CHROME_PROFILES,
                        risk=RiskLevel.REVIEW,
                        size_bytes=size,
                        selected=False,
                        details={"profile_dir": prof_dir, "name": display_name, "email": email}
                    )
                )
    except Exception:
        pass

    # Sort largest first
    items.sort(key=lambda x: x.size_bytes, reverse=True)
    return items
