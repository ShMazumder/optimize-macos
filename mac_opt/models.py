from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Callable


class RiskLevel(Enum):
    SAFE = "SAFE"        # 🟢 Pure disposable caches, auto-regenerates
    REVIEW = "REVIEW"    # 🟡 Profiles, history, simulator runtimes
    CAUTION = "CAUTION"  # 🔴 Project build outputs, archives, developer data

    @property
    def badge(self) -> str:
        if self == RiskLevel.SAFE:
            return "[bold green]🟢 SAFE[/bold green]"
        elif self == RiskLevel.REVIEW:
            return "[bold yellow]🟡 REVIEW[/bold yellow]"
        else:
            return "[bold red]🔴 CAUTION[/bold red]"


class CleanableCategory(Enum):
    QUICK_CLEAN = "Quick Clean"
    DEVELOPER = "Developer Tools"
    CHROME_PROFILES = "Chrome Profiles"
    AI_IDE = "AI & IDEs"
    LARGE_FILES = "Large Files"


@dataclass
class CleanableItem:
    id: str
    title: str
    description: str
    path: str
    category: CleanableCategory
    risk: RiskLevel
    size_bytes: int = 0
    selected: bool = False
    details: Dict[str, Any] = field(default_factory=dict)
    custom_action: Optional[str] = None  # e.g. "simctl", "brew"

    @property
    def size_human(self) -> str:
        return format_bytes(self.size_bytes)


@dataclass
class DiskStats:
    total_bytes: int
    free_bytes: int
    used_bytes: int
    container_name: str = "Macintosh HD"

    @property
    def percent_used(self) -> float:
        if self.total_bytes == 0:
            return 0.0
        return (self.used_bytes / self.total_bytes) * 100

    @property
    def total_human(self) -> str:
        return format_bytes(self.total_bytes)

    @property
    def free_human(self) -> str:
        return format_bytes(self.free_bytes)

    @property
    def used_human(self) -> str:
        return format_bytes(self.used_bytes)


def format_bytes(num_bytes: int) -> str:
    """Format bytes into human readable KB, MB, GB."""
    if num_bytes <= 0:
        return "0 B"
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if abs(num_bytes) < 1024.0:
            return f"{num_bytes:3.1f} {unit}"
        num_bytes /= 1024.0
    return f"{num_bytes:.1f} PB"
