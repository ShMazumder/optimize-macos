import os
from typing import List
from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel
from mac_opt.utils import get_path_size


def scan_ai_and_ides() -> List[CleanableItem]:
    """Scan AI tools and IDE caches (Antigravity, Claude, VS Code)."""
    home = os.path.expanduser("~")
    items: List[CleanableItem] = []

    # 1. Antigravity Browser Recordings
    rec_path = os.path.join(home, ".gemini", "antigravity-ide", "browser_recordings")
    rec_size = get_path_size(rec_path)
    items.append(
        CleanableItem(
            id="ai_antigravity_recordings",
            title="Antigravity Browser Agent Recordings",
            description="WebP screen recording videos captured during autonomous web tasks",
            path=rec_path,
            category=CleanableCategory.AI_IDE,
            risk=RiskLevel.SAFE,
            size_bytes=rec_size,
            selected=(rec_size > 0)
        )
    )

    # 2. Antigravity Agent Browser Profile Cache
    agent_browser_cache = os.path.join(home, ".gemini", "antigravity-browser-profile", "Default", "Cache")
    browser_cache_size = get_path_size(agent_browser_cache)
    items.append(
        CleanableItem(
            id="ai_antigravity_browser_cache",
            title="Antigravity Internal Browser Cache",
            description="Temporary HTTP cache from web pages visited by browser subagents",
            path=agent_browser_cache,
            category=CleanableCategory.AI_IDE,
            risk=RiskLevel.SAFE,
            size_bytes=browser_cache_size,
            selected=(browser_cache_size > 10 * 1024 * 1024)
        )
    )

    # 3. Antigravity Brain Scratch & Temporary Scripts
    brain_root = os.path.join(home, ".gemini", "antigravity-ide", "brain")
    scratch_size = 0
    if os.path.exists(brain_root):
        try:
            for entry in os.scandir(brain_root):
                if entry.is_dir():
                    s_path = os.path.join(entry.path, "scratch")
                    if os.path.exists(s_path):
                        scratch_size += get_path_size(s_path)
        except Exception:
            pass

    items.append(
        CleanableItem(
            id="ai_antigravity_brain_scratch",
            title="Antigravity Workspace Scratch Scripts & Images",
            description="Intermediate test scripts, mockups, and execution scratchpads from completed tasks",
            path=brain_root,
            category=CleanableCategory.AI_IDE,
            risk=RiskLevel.SAFE,
            size_bytes=scratch_size,
            selected=(scratch_size > 10 * 1024 * 1024),
            custom_action="antigravity_scratch"
        )
    )

    # 4. Claude App Caches
    claude_cache = os.path.join(home, "Library", "Caches", "com.anthropic.claudefordesktop")
    if not os.path.exists(claude_cache):
        claude_cache = os.path.join(home, "Library", "Application Support", "Claude", "Cache")
    claude_size = get_path_size(claude_cache)
    items.append(
        CleanableItem(
            id="ai_claude_cache",
            title="Claude Desktop App Cache",
            description="Electron web view and asset caches for Claude desktop",
            path=claude_cache,
            category=CleanableCategory.AI_IDE,
            risk=RiskLevel.SAFE,
            size_bytes=claude_size,
            selected=(claude_size > 20 * 1024 * 1024)
        )
    )

    # 5. VS Code Caches
    vscode_cache = os.path.join(home, "Library", "Caches", "com.microsoft.VSCode")
    vscode_size = get_path_size(vscode_cache)
    items.append(
        CleanableItem(
            id="ide_vscode_cache",
            title="Visual Studio Code Cache",
            description="Editor workspace cache, telemetry logs, and GPU caches",
            path=vscode_cache,
            category=CleanableCategory.AI_IDE,
            risk=RiskLevel.SAFE,
            size_bytes=vscode_size,
            selected=(vscode_size > 50 * 1024 * 1024)
        )
    )

    return items
