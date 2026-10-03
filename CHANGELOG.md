# Changelog

All notable changes to `mac-opt` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-10-03

### Added
* **Real-time APFS Storage Gauge:** Live container total, used, free, and color-coded utilization gauge widget.
* **Quick Clean Module:** Safe-to-clean temporary caches (Chrome web cache, Python UV/pip, Node NPM, Homebrew bottles, Dart language analyzer, and macOS Trash).
* **Developer Tools Module:** Xcode iOS Simulator runtime detection & deletion (20–30 GB reclaimable), simulator device containers cleanup (`simctl erase all`), Xcode DerivedData, and Android Gradle caches.
* **Chrome Profile Explorer:** Automated parser for Chrome's `Local State` listing all profiles with human-readable account names, user emails, and exact disk usage.
* **AI & IDE History Cleaner:** Purging Antigravity browser automation WebP recordings (`browser_recordings`), scratch code, and Claude / VS Code desktop caches.
* **Large Files Scanner:** Scans user folders (`~/Downloads`, `~/Documents`, `~/Desktop`) for files > 100 MB with compressibility detection.
* **Safety Architecture:** Explicit risk badges (🟢 SAFE, 🟡 REVIEW, 🔴 CAUTION), dry-run preview mode (`D`), and confirmation dialogs before deletion.
* **Interactive TUI:** Built with Textual and Rich, featuring full keyboard and mouse support, tabbed navigation, and modern dark mode styling.
