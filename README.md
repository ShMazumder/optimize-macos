# 🚀 mac-opt — Developer-First macOS Storage Optimizer & Disk Cleaner TUI

[![Release](https://img.shields.io/github/v/release/ShMazumder/optimize-macos?style=for-the-badge&color=38bdf8)](https://github.com/ShMazumder/optimize-macos/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![macOS](https://img.shields.io/badge/macOS-APFS%20Optimized-0284c7?style=for-the-badge&logo=apple)](https://apple.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![Built With Textual](https://img.shields.io/badge/Built%20With-Textual-059669?style=for-the-badge)](https://textual.textualize.io/)

> **Reclaim 10–30+ GB of hidden macOS "System Data", Xcode iOS Simulator runtimes, multi-profile Chrome bloat, and orphaned developer caches with 100% transparency, zero subscriptions, and non-destructive defaults.**

---

## ⚡ The Problem: Where Did Your Mac's Storage Go?

If your Mac storage settings vaguely report **40–60 GB of "System Data"**, macOS is hiding developer bloat:
* **Xcode iOS Simulator Runtimes** silently mount **20–30+ GB** in `/Library/Developer/CoreSimulator/Volumes`.
* **Google Chrome User Profiles** accumulate **5–15 GB** across multiple profiles without clearing IndexedDB and cache.
* **Package Managers** (`uv`, `pip`, `npm`, `Homebrew`, `Gradle`) hoard gigabytes of orphaned wheels and build caches.
* Proprietary GUI disk cleaners charge hefty annual subscriptions or delete files without showing you what's being removed.

`mac-opt` is an open-source, keyboard-driven Terminal User Interface (TUI) engineered for macOS and software developers to audit, visualize, and safely purge exact storage bottlenecks.

---

## 🆚 Why `mac-opt`?

| Feature | macOS System Settings | Proprietary GUI Cleaners | `mac-opt` |
| :--- | :---: | :---: | :---: |
| **Price** | Free (Built-in) | $39–$89/year subscription | **100% Free & Open Source** |
| **Transparency** | Vague labels ("System Data") | Opaque "Smart Scan" | **Exact paths & byte counts** |
| **Xcode Simulator Cleaner** | Manual / Difficult | ❌ Ignored | **1-Click 20–30 GB Prune** |
| **Chrome Multi-Profile Scanner** | ❌ None | ❌ Deletes cookies & logins | **Maps Profiles to Names & Emails** |
| **Developer Caches (uv, npm, pip)** | ❌ Ignored | Partial | **Full Developer Engine** |
| **Dry-Run Preview Mode** | ❌ No | ❌ No | **Press `D` to Preview Before Deleting** |
| **Interface** | Slow GUI Indexer | Heavy Background Daemons | **Blazing Fast Terminal TUI** |

---

## 💻 Visual Preview

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  mac-opt: macOS Storage Optimizer (v0.1.0)           [Free: 32 GB | 26% Used]│
├──────────────────────────────────────────────────────────────────────────────┤
│ [⚡ Quick Clean]  [🛠️ Developer]  [🌐 Chrome Profiles]  [🤖 AI & IDEs] [📁 >100M]│
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  [X]   37.7 MB  🟢 SAFE  Google Chrome Web Cache                             │
│  [X]   24.0 MB  🟢 SAFE  Python UV Package Cache                             │
│  [X]  178.3 MB  🟢 SAFE  Node NPM Package Cache                              │
│  [ ]   30.0 GB  🟡 REVIEW iOS Simulator Runtime (iOS 18.6)                   │
│  [ ]    1.7 GB  🟡 REVIEW Chrome: Shazzad Hossain (shmazumder23@gmail.com)    │
│  [ ]    1.1 GB  🟡 REVIEW Chrome: CSE (cselab.fu@gmail.com)                  │
│                                                                              │
│  ──────────────────────────────────────────────────────────────────────────  │
│  Selected: 3 items  │  Reclaimable Space: 240 MB  │  [C] Clean  [D] Dry Run  │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Space] Toggle  │ [A] Select Safe  │ [D] Dry Run  │ [C] Clean  │ [Q] Quit    │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📥 Installation & Running

### Option 1: Clone & Run with `uv` (Recommended — Instant Zero-Setup)

[`uv`](https://github.com/astral-sh/uv) automatically runs `mac-opt` with inline dependencies without needing manual virtualenv creation:

```bash
# 1. Clone the repository
git clone https://github.com/ShMazumder/optimize-macos.git
cd optimize-macos

# 2. Run immediately (uv handles all dependencies automatically)
./mac-opt
```

*(Or run `uv run mac-opt`)*.

---

### Option 2: Standard Python Virtual Environment

```bash
# 1. Clone the repository
git clone https://github.com/ShMazumder/optimize-macos.git
cd optimize-macos

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install textual rich psutil

# 4. Launch the application
python3 main.py
```

---

### Option 3: Create a Global Terminal Shortcut

To launch `mac-opt` from anywhere on your Mac, add an alias to your `~/.zshrc`:

```bash
echo 'alias mac-opt="'"$(pwd)"'/mac-opt"' >> ~/.zshrc
source ~/.zshrc
```

Now simply type `mac-opt` from any terminal directory!

---

## 🌟 Core Modules

### 1. 💾 Real-Time APFS Storage Gauge
* Live APFS container breakdown with Total, Used, and Free space.
* Color-coded health indicators:
  * 🟢 **Healthy** (< 50% capacity used)
  * 🟡 **Moderate** (50% – 75% capacity used)
  * 🔴 **Critical Warning** (> 75% capacity used)

### 2. ⚡ Quick Clean (Zero-Risk Caches)
Purges files that regenerate on demand without logging you out or touching personal documents:
* **Google Chrome Web Cache:** Images, scripts, media caches (keeps all saved logins, cookies, and bookmarks intact).
* **Package Manager Caches:** Python `uv`, `pip`, Node `npm`, and Homebrew download bottles (`brew cleanup -s`).
* **Dart / Flutter Analyzer Cache:** `~/.dartServer` indexing caches.
* **macOS Trash:** `~/.Trash` permanent deletion.
* **User Diagnostics & Logs:** `~/Library/Logs`.

### 3. 🛠️ Developer Engine (The Heavy Lifters)
* **iOS Simulator Runtimes:** Detects Xcode simulator runtimes (such as iOS 18.x) and allows 1-click removal of 20–30 GB images from "System Data".
* **Simulator Device Containers:** Safely erases test data in simulated iPhones/iPads via `xcrun simctl erase all`.
* **Xcode Build Artifacts:** Cleans `DerivedData` and iOS Device Crash Logs.
* **Android & Flutter Build Tools:** Gradle build caches and CocoaPods spec caches.

### 4. 🌐 Chrome Profile Explorer
* Reads Chrome's `Local State` file automatically.
* Lists all Chrome profiles with:
  * Profile display name
  * Associated user email
  * Exact disk footprint on your SSD
* Selectively delete inactive, test, or old project profiles directly from the TUI.

### 5. 🤖 AI & IDE Cache Pruner
* **Antigravity IDE:** Prunes browser agent WebP recordings (`browser_recordings`), old task scratch code, and internal Chromium caches.
* **Claude Desktop:** Electron cache pruner.
* **VS Code:** GPU and editor cache pruner.

### 6. 📁 Large Files Scanner (> 100 MB)
* Automatically scans `~/Downloads`, `~/Documents`, and `~/Desktop` for files exceeding 100 MB.
* Identifies compressible database dumps (SQL, JSON, CSV, log files) and loose installers.

---

## ⌨️ Keyboard & Mouse Controls

| Key | Action |
| :--- | :--- |
| `Space` / `Click` | Toggle checkbox for current highlighted item |
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

## 📂 Project Architecture

```
optimize/
├── mac-opt                 # Standalone executable entrypoint (PEP 723)
├── pyproject.toml          # Project configuration & dependencies
├── CHANGELOG.md            # Release version history
├── README.md               # Documentation & SEO guide
├── AGENTS.md               # Context & roadmap for AI coding agents
└── mac_opt/
    ├── __init__.py         # Package versioning (v0.1.0)
    ├── __main__.py         # CLI entrypoint forwarding
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

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [Issues page](https://github.com/ShMazumder/optimize-macos/issues) or read [`AGENTS.md`](AGENTS.md) for architectural guidelines and future roadmap goals.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<p align="center">
  Crafted with ❤️ for macOS users and developers.
</p>
