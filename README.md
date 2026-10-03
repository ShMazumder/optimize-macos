# 🚀 mac-opt — macOS Storage Optimizer TUI

A modern, fast, keyboard- and mouse-navigable Terminal User Interface (TUI) designed specifically for macOS users and developers to audit, visualize, and safely reclaim gigabytes of disk space.

![mac-opt preview](https://img.shields.io/badge/macOS-APFS%20Storage%20Optimizer-0284c7?style=for-the-badge&logo=apple)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Textual](https://img.shields.io/badge/Built%20With-Textual-green?style=for-the-badge)

---

## ⚡ Quick Start

You can run `mac-opt` directly in your terminal using `uv`:

```bash
# From the project directory
./mac-opt
```

Or run via standard Python virtual environment:

```bash
uv run mac-opt
```

---

## 🌟 Key Features

### 1. 💾 Real-Time APFS Storage Gauge
* Live APFS container breakdown with Total, Used, and Free space.
* Color-coded health indicators:
  * 🟢 **Healthy** (< 50% capacity used)
  * 🟡 **Moderate** (50% – 75% capacity used)
  * 🔴 **Critical Warning** (> 75% capacity used)

### 2. ⚡ Quick Clean (Zero-Risk Caches)
Purges files that regenerate on demand without logging you out or deleting personal documents:
* **Google Chrome Web Cache:** Images, scripts, media caches (keeps all saved logins, cookies, and bookmarks intact).
* **Package Manager Caches:** Python `uv`, `pip`, Node `npm`, and Homebrew download bottles.
* **Dart / Flutter Analyzer Cache:** `~/.dartServer` indexing caches.
* **macOS Trash:** `~/.Trash` permanent deletion.
* **System & Diagnostic Logs:** `~/Library/Logs`.

### 3. 🛠️ Developer Engine
* **iOS Simulator Runtimes:** Detects Xcode simulator runtimes (such as iOS 18.x) and allows 1-click removal of 20–30 GB images from "System Data".
* **Simulator Device Containers:** Safely erases test data in simulated iPhones/iPads via `xcrun simctl erase all`.
* **Xcode Build Artifacts:** Cleans `DerivedData` and iOS Device Crash Logs.
* **Android & Flutter Build Tools:** Gradle build caches and CocoaPods spec caches.

### 4. 🌐 Chrome Profile Explorer
* Reads Chrome's `Local State` file automatically.
* Lists all 29+ Chrome profiles with:
  * Account display name
  * User email
  * Disk usage per profile
* Selectively delete inactive, test, or old project profiles directly from the TUI.

### 5. 🤖 AI & IDEs
* **Antigravity IDE:** Prunes browser agent WebP recordings (`browser_recordings`), old task scratch code, and internal Chromium caches.
* **Claude Desktop:** Electron cache pruner.
* **VS Code:** GPU and editor cache pruner.

### 6. 📁 Large Files Scanner (> 100 MB)
* Automatically scans `~/Downloads`, `~/Documents`, and `~/Desktop` for files exceeding 100 MB.
* Identifies compressible database dumps (SQL, JSON, CSV, log files) and loose installers.

---

## ⌨️ Keyboard Shortcuts & Controls

| Key | Action |
| :--- | :--- |
| `Space` | Toggle checkbox for current highlighted item |
| `A` | **Select All Safe Items** (instantly checks all 🟢 zero-risk caches) |
| `N` | **Deselect All** |
| `D` | **Dry Run** (previews exact reclaimable space without deleting anything) |
| `C` or `Enter` | **Clean Selected Items** (opens confirmation modal) |
| `R` | **Rescan** (re-calculates disk sizes and reloads all categories) |
| `Q` | **Quit** |
| `Mouse Click` | Full mouse support for switching tabs, clicking checkboxes, and buttons |

---

## 🛡️ Safety Architecture

Every cleanable item is tagged with a clear risk level:
* 🟢 **SAFE:** Pure disposable caches that re-download or regenerate automatically. Zero user data loss.
* 🟡 **REVIEW:** Profiles, chat history, or simulator runtimes. May require re-downloading or re-login.
* 🔴 **CAUTION:** Developer build products and project archives.

---

## 📂 Project Structure

```
optimize/
├── mac-opt                 # Executable entrypoint script
├── pyproject.toml          # Project configuration & dependencies
├── README.md               # Documentation
└── mac_opt/
    ├── app.py              # Main Textual App & event loop
    ├── cleaner.py          # Safe deletion & dry-run execution engine
    ├── models.py           # CleanableItem, RiskLevel, DiskStats data models
    ├── styles.tcss         # Dark-mode terminal CSS stylesheet
    ├── utils.py            # Recursive directory size calculations
    ├── scanners/
    │   ├── system.py       # APFS container & diskutil scanner
    │   ├── caches.py       # Quick caches (Chrome, uv, npm, brew, Trash)
    │   ├── developer.py    # Xcode, simctl, Android, Gradle, CocoaPods
    │   ├── chrome.py       # Chrome profile explorer with Local State parser
    │   ├── ai_ide.py       # Antigravity, Claude, VS Code caches
    │   └── large_files.py  # >100MB file scanner in user folders
    └── widgets/
        ├── disk_gauge.py   # APFS visual capacity gauge widget
        └── confirm_modal.py# Confirmation & dry-run modal screens
```
