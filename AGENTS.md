# 🤖 AGENTS.md — AI Agent Guidance for `mac-opt`

Welcome, AI Agent! This document provides context, architectural design principles, safety guidelines, and the future development roadmap for the `mac-opt` codebase. Read this file before proposing or executing modifications to this project.

---

## 1. Project Overview & Context

`mac-opt` is a modern Terminal User Interface (TUI) utility built with **Python 3**, **Textual**, and **Rich** specifically engineered for macOS users and software developers.

### The Problem It Solves
* macOS System Settings vaguely labels tens of gigabytes under **"System Data"** and **"Documents"** without detailing what is actually consuming space.
* Developer workflows silently accumulate enormous caches:
  * Xcode iOS Simulator disk images and mounted volumes (`/Library/Developer/CoreSimulator`) easily consume 20–30+ GB.
  * Google Chrome user profiles (`~/Library/Application Support/Google/Chrome`) grow to 5–15 GB across multiple profiles.
  * Package managers (`uv`, `pip`, `npm`, `Homebrew`, `Gradle`) leave gigabytes of orphaned wheels, archives, and build artifacts.
* Existing GUI tools are often proprietary, subscription-based, or opaque about what they delete.

`mac-opt` provides an open-source, developer-friendly, keyboard-driven TUI that scans these exact pain points, previews reclaimable space with 100% transparency, and cleans them safely.

---

## 2. Tech Stack & Execution Model

* **Language:** Python `>= 3.10` (compatible through Python 3.14).
* **Package / Environment Manager:** [`uv`](https://github.com/astral-sh/uv) (recommended) or standard `pip`/`venv`.
* **UI Framework:** [Textual](https://textual.textualize.io/) (`textual>=0.80.0`) for reactive layouts, async event loops, keyboard shortcuts, and mouse support.
* **Terminal Formatting:** [Rich](https://rich.readthedocs.io/) (`rich>=13.0.0`) for gauges, tables, and markup.
* **System Metrics:** `psutil>=5.9.0` and native macOS CLI wrappers (`diskutil`, `xcrun simctl`).
* **PEP 723 Script:** The `./mac-opt` file has inline script metadata so it can run via `uv run mac-opt` or directly `./mac-opt` without manual virtualenv activation.

---

## 3. Codebase Architecture

```
optimize/
├── mac-opt                 # Standalone executable entrypoint (PEP 723)
├── pyproject.toml          # Project metadata, dependencies, scripts
├── CHANGELOG.md            # Release version history
├── README.md               # User-facing documentation
├── AGENTS.md               # Instructions & context for AI agents (this file)
└── mac_opt/
    ├── __init__.py         # Defines __version__ = "0.1.0"
    ├── __main__.py         # CLI invocation forwarding to app.py:main
    ├── app.py              # Main Textual App, reactive state, tab views, keybindings
    ├── models.py           # Core dataclasses: CleanableItem, DiskStats, RiskLevel, CleanableCategory
    ├── utils.py            # Fast recursive directory & file size computation
    ├── cleaner.py          # Deletion & dry-run execution engine with custom action handlers
    ├── styles.tcss         # Dark-mode terminal CSS stylesheet
    ├── scanners/           # Modular scanning plugins
    │   ├── system.py       # APFS container & volume usage via diskutil info /
    │   ├── caches.py       # User caches: Chrome cache, uv, npm, pip, brew, Trash, Logs
    │   ├── developer.py    # Xcode simctl runtimes, simulator devices, DerivedData, Gradle
    │   ├── chrome.py       # Parses Chrome Local State for profile names, emails, and sizes
    │   ├── ai_ide.py       # Antigravity recordings, scratch code, Claude, VS Code caches
    │   └── large_files.py  # User files >100MB in Downloads, Documents, Desktop
    └── widgets/
        ├── disk_gauge.py   # APFS visual capacity gauge widget
        └── confirm_modal.py# Modal confirmation & dry-run preview dialogs
```

---

## 4. 🚨 Safety Principles (CRITICAL FOR AGENTS)

When modifying or expanding cleaners, agents MUST adhere to these non-negotiable rules:

1. **Non-Destructive Defaults:**
   * Only items with `RiskLevel.SAFE` AND `size_bytes > 0` may be pre-selected by default.
   * Items with `RiskLevel.REVIEW` or `RiskLevel.CAUTION` must **NEVER** be selected by default.
2. **Never Touch User Project Code or Databases:**
   * Avoid blanket deletions in `/Applications/XAMPP` (user websites in `htdocs` and MySQL databases in `var/mysql` must be protected).
   * Do not delete git repositories, working directories, or document files without explicit individual confirmation.
3. **Respect Browser Profiles vs. Browser Caches:**
   * `~/Library/Caches/Google` contains pure temporary web cache. Safe to delete.
   * `~/Library/Application Support/Google/Chrome/<Profile>` contains sessions, cookies, logins, and extensions. Deleting these logs users out. Categorize strictly as `RiskLevel.REVIEW`.
4. **Always Implement Dry-Run Parity:**
   * Every cleaning action in `cleaner.py` MUST support `dry_run=True` to calculate and log the exact byte count before any real filesystem deletion occurs.

---

## 5. Development & Testing Protocols

### Running the App Locally
```bash
# Via uv (recommended)
uv run mac-opt

# Or directly through the executable script
./mac-opt
```

### Checking Program Version & Help
```bash
./mac-opt --version
./mac-opt --help
```

### Headless / Scanner Unit Testing
Because Textual requires a TTY terminal, test scanner modules headlessly via Python:
```bash
uv run python -c "
from mac_opt.scanners.system import get_disk_stats
from mac_opt.scanners.caches import scan_quick_caches
from mac_opt.scanners.developer import scan_developer_tools
from mac_opt.scanners.chrome import scan_chrome_profiles
from mac_opt.scanners.ai_ide import scan_ai_and_ides
from mac_opt.scanners.large_files import scan_large_files

print(get_disk_stats())
print('Caches:', len(scan_quick_caches()))
print('Dev:', len(scan_developer_tools()))
print('Chrome:', len(scan_chrome_profiles()))
print('AI/IDE:', len(scan_ai_and_ides()))
print('Large Files:', len(scan_large_files(100)))
"
```

---

## 6. Future Developments & Roadmap

When working on upcoming phases of `mac-opt`, prioritize the following enhancements:

### High Priority
* [ ] **Headless CLI Command:** Add `--clean-safe` flag (e.g., `mac-opt --clean-safe --dry-run` or `mac-opt --clean-safe -y`) so users can automate routine cache cleanups via cron or shell scripts without opening the TUI.
* [ ] **Docker Engine Scanner:** Scan Docker desktop VM disk image (`~/Library/Containers/com.docker.docker`), dangling images, stopped containers, and build cache (`docker system df`).
* [ ] **Homebrew Packaging:** Create a formula for `brew install mac-opt` or tap distribution.

### Medium Priority
* [ ] **Orphaned `node_modules` Scanner:** Traversal engine to find abandoned `node_modules` folders in inactive coding projects older than 60 days.
* [ ] **1-Click Gzip Compressor:** In the Large Files tab, allow pressing `Z` to compress selected files (e.g. `.sql`, `.log`, `.csv`) with `gzip` directly from the TUI.
* [ ] **Automated Trash Schedule:** Show how old items in `~/.Trash` are, with a toggle to purge only items older than 30 days.

### Low Priority / Nice-to-Have
* [ ] **Export Audit Report:** Export markdown / JSON audit reports to `~/Desktop` or stdout (`mac-opt --audit --json`).
* [ ] **Custom Exclusion Rules:** Allow configuring a `~/.config/mac-opt/ignore.json` for paths to never scan or touch.

---

## 7. How to Add a New Scanner Plugin

1. Create a function in `mac_opt/scanners/<your_scanner>.py` that returns a `List[CleanableItem]`.
2. Assign each item a clear `CleanableCategory`, `RiskLevel`, and path.
3. If the item requires a specific CLI command rather than `shutil.rmtree` (e.g. `docker builder prune`), specify `custom_action="your_action"` and add the handler to `clean_items()` in `mac_opt/cleaner.py`.
4. Import and register the scanner in `mac_opt/app.py` under `run_full_scan()`.
5. Update `CHANGELOG.md` with the new capability.
