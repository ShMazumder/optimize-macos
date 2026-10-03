import os
from typing import List
from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel
from mac_opt.utils import get_path_size


def scan_quick_caches() -> List[CleanableItem]:
    """Scan all safe-to-clean temporary caches."""
    home = os.path.expanduser("~")
    items: List[CleanableItem] = []

    targets = [
        {
            "id": "cache_chrome_web",
            "title": "Google Chrome Web Cache",
            "desc": "Cached web images, stylesheets, and scripts (does not log you out)",
            "path": os.path.join(home, "Library", "Caches", "Google"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "cache_uv",
            "title": "Python UV Package Cache",
            "desc": "Cached Python wheels and tool runtimes downloaded by uv",
            "path": os.path.join(home, ".cache", "uv"),
            "risk": RiskLevel.SAFE,
            "custom_action": "uv",
        },
        {
            "id": "cache_npm",
            "title": "Node NPM Package Cache",
            "desc": "Cached tarballs and metadata from npm install",
            "path": os.path.join(home, ".npm"),
            "risk": RiskLevel.SAFE,
            "custom_action": "npm",
        },
        {
            "id": "cache_pip",
            "title": "Python Pip Cache",
            "desc": "Downloaded python wheel packages from pip install",
            "path": os.path.join(home, "Library", "Caches", "pip"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "cache_brew",
            "title": "Homebrew Download Cache",
            "desc": "Downloaded bottles and tarballs from brew install",
            "path": os.path.join(home, "Library", "Caches", "Homebrew"),
            "risk": RiskLevel.SAFE,
            "custom_action": "brew",
        },
        {
            "id": "cache_dart",
            "title": "Dart Language Analyzer Cache",
            "desc": "Analysis server indices generated for Flutter and Dart projects",
            "path": os.path.join(home, ".dartServer"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "trash_bin",
            "title": "macOS Trash",
            "desc": "Files waiting in the Trash bin waiting to be permanently erased",
            "path": os.path.join(home, ".Trash"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "cache_google_updater_crx",
            "title": "Google Updater Extension CRX Cache",
            "desc": "Downloaded .crx archive updates for Chrome extensions",
            "path": os.path.join(home, "Library", "Application Support", "Google", "GoogleUpdater", "crx_cache"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "cache_chrome_component_crx",
            "title": "Chrome Component Extension Cache",
            "desc": "Temporary unpack directories for built-in browser components",
            "path": os.path.join(home, "Library", "Application Support", "Google", "Chrome", "component_crx_cache"),
            "risk": RiskLevel.SAFE,
        },
        {
            "id": "logs_user",
            "title": "User Application Logs",
            "desc": "Crash reports and diagnostics logs in ~/Library/Logs",
            "path": os.path.join(home, "Library", "Logs"),
            "risk": RiskLevel.SAFE,
        },
    ]

    for t in targets:
        size = get_path_size(t["path"])
        # Even if 0 or small, show it so the user can verify
        items.append(
            CleanableItem(
                id=t["id"],
                title=t["title"],
                description=t["desc"],
                path=t["path"],
                category=CleanableCategory.QUICK_CLEAN,
                risk=t["risk"],
                size_bytes=size,
                selected=(size > 0),
                custom_action=t.get("custom_action")
            )
        )

    return items
