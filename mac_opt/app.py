import os
from typing import List, Dict
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import (
    Header,
    Footer,
    Static,
    TabbedContent,
    TabPane,
    SelectionList,
    Button,
    Label,
)
from textual.binding import Binding
from textual.widgets.selection_list import Selection

from mac_opt.models import CleanableItem, CleanableCategory, RiskLevel, format_bytes
from mac_opt.scanners.system import get_disk_stats
from mac_opt.scanners.caches import scan_quick_caches
from mac_opt.scanners.developer import scan_developer_tools
from mac_opt.scanners.chrome import scan_chrome_profiles
from mac_opt.scanners.ai_ide import scan_ai_and_ides
from mac_opt.scanners.large_files import scan_large_files
from mac_opt.cleaner import clean_items
from mac_opt.widgets.disk_gauge import DiskGaugeWidget
from mac_opt.widgets.confirm_modal import ConfirmCleanModal


class MacStorageOptimizerApp(App):
    """Modern macOS Storage Optimizer Terminal UI."""

    CSS_PATH = "styles.tcss"
    TITLE = "mac-opt 🚀 macOS Storage Optimizer"

    BINDINGS = [
        Binding("a", "select_all_safe", "Select Safe", show=True),
        Binding("n", "deselect_all", "Deselect All", show=True),
        Binding("d", "dry_run", "Dry Run", show=True),
        Binding("c", "clean_selected", "Clean Selected", show=True),
        Binding("r", "refresh_scan", "Rescan", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.disk_stats = get_disk_stats()
        self.items_by_id: Dict[str, CleanableItem] = {}
        self.category_items: Dict[CleanableCategory, List[CleanableItem]] = {
            cat: [] for cat in CleanableCategory
        }

    def compose(self) -> ComposeResult:
        with Vertical(id="header_container"):
            yield Static("🚀 [bold #38bdf8]mac-opt[/bold #38bdf8] — [dim]macOS Storage Audit & Optimizer[/dim]", id="header_title")
            yield DiskGaugeWidget(self.disk_stats, id="disk_gauge")

        with TabbedContent(id="tabs"):
            with TabPane("⚡ Quick Clean", id="tab_quick"):
                yield SelectionList[str](id="list_quick")
            with TabPane("🛠️ Developer", id="tab_dev"):
                yield SelectionList[str](id="list_dev")
            with TabPane("🌐 Chrome Profiles", id="tab_chrome"):
                yield SelectionList[str](id="list_chrome")
            with TabPane("🤖 AI & IDEs", id="tab_ai"):
                yield SelectionList[str](id="list_ai")
            with TabPane("📁 Large Files (>100M)", id="tab_large"):
                yield SelectionList[str](id="list_large")

        yield Static("Scanning storage targets...", id="footer_summary")
        yield Footer()

    def on_mount(self) -> None:
        self.run_full_scan()

    def run_full_scan(self) -> None:
        """Run all scanners and populate the selection lists."""
        self.query_one("#footer_summary", Static).update("⏳ Scanning directories and calculating sizes...")
        self.disk_stats = get_disk_stats()
        gauge = self.query_one("#disk_gauge", DiskGaugeWidget)
        gauge.update_stats(self.disk_stats)

        # 1. Quick Caches
        quick_items = scan_quick_caches()
        # 2. Developer Tools
        dev_items = scan_developer_tools()
        # 3. Chrome Profiles
        chrome_items = scan_chrome_profiles()
        # 4. AI & IDEs
        ai_items = scan_ai_and_ides()
        # 5. Large Files
        large_items = scan_large_files(min_size_mb=100)

        self.category_items[CleanableCategory.QUICK_CLEAN] = quick_items
        self.category_items[CleanableCategory.DEVELOPER] = dev_items
        self.category_items[CleanableCategory.CHROME_PROFILES] = chrome_items
        self.category_items[CleanableCategory.AI_IDE] = ai_items
        self.category_items[CleanableCategory.LARGE_FILES] = large_items

        self.items_by_id.clear()
        for cat_list in self.category_items.values():
            for item in cat_list:
                self.items_by_id[item.id] = item

        # Populate lists
        self.populate_list("list_quick", quick_items)
        self.populate_list("list_dev", dev_items)
        self.populate_list("list_chrome", chrome_items)
        self.populate_list("list_ai", ai_items)
        self.populate_list("list_large", large_items)

        self.update_summary()

    def populate_list(self, list_id: str, items: List[CleanableItem]) -> None:
        sel_list = self.query_one(f"#{list_id}", SelectionList)
        sel_list.clear_options()

        selections = []
        for item in items:
            badge = item.risk.badge
            size_badge = f"[bold cyan]{item.size_human:>8}[/bold cyan]"
            label = f"{size_badge}  {badge}  [bold]{item.title}[/bold]\n         [dim]{item.description}[/dim]"
            
            # Default select only SAFE items with size > 0
            is_checked = (item.risk == RiskLevel.SAFE and item.size_bytes > 0)
            item.selected = is_checked

            selections.append(Selection(label, item.id, initial_state=is_checked))

        sel_list.add_options(selections)

    def on_selection_list_selected_changed(self, event: SelectionList.SelectedChanged) -> None:
        """Handle checkbox state toggles."""
        selected_ids = set(event.selection_list.selected)
        # Update selection state for items in this list
        for item in self.items_by_id.values():
            # If the item belongs to this list's options
            for opt in event.selection_list._options:
                if opt.value == item.id:
                    item.selected = (item.id in selected_ids)

        self.update_summary()

    def update_summary(self) -> None:
        selected = [item for item in self.items_by_id.values() if item.selected]
        reclaimable_bytes = sum(item.size_bytes for item in selected)
        
        text = (
            f"[bold cyan]Selected:[/bold cyan] [bold yellow]{len(selected)} items[/bold yellow]  │  "
            f"[bold cyan]Reclaimable Space:[/bold cyan] [bold green]{format_bytes(reclaimable_bytes)}[/bold green]  │  "
            f"[dim]Press [bold]C[/bold] to Clean, [bold]D[/bold] for Dry Run, [bold]A[/bold] to Select Safe[/dim]"
        )
        self.query_one("#footer_summary", Static).update(text)

    def action_select_all_safe(self) -> None:
        """Select all items marked SAFE."""
        for item in self.items_by_id.values():
            if item.risk == RiskLevel.SAFE and item.size_bytes > 0:
                item.selected = True

        for list_id in ["list_quick", "list_dev", "list_chrome", "list_ai", "list_large"]:
            try:
                sel_list = self.query_one(f"#{list_id}", SelectionList)
                safe_ids = [
                    item.id for item in self.items_by_id.values()
                    if item.risk == RiskLevel.SAFE and item.size_bytes > 0
                ]
                sel_list.select_all()
            except Exception:
                pass

        self.update_summary()

    def action_deselect_all(self) -> None:
        """Deselect all items across all tabs."""
        for item in self.items_by_id.values():
            item.selected = False

        for list_id in ["list_quick", "list_dev", "list_chrome", "list_ai", "list_large"]:
            try:
                sel_list = self.query_one(f"#{list_id}", SelectionList)
                sel_list.deselect_all()
            except Exception:
                pass

        self.update_summary()

    def action_dry_run(self) -> None:
        """Run a dry-run preview on selected items."""
        selected = [item for item in self.items_by_id.values() if item.selected]
        if not selected:
            self.notify("No items selected for dry run!", severity="warning")
            return

        def handle_dry_run(confirmed: bool) -> None:
            if confirmed:
                freed, logs = clean_items(selected, dry_run=True)
                self.notify(f"Dry run complete: Would reclaim {format_bytes(freed)}", severity="information")

        self.push_screen(ConfirmCleanModal(selected, dry_run=True), handle_dry_run)

    def action_clean_selected(self) -> None:
        """Prompt confirmation and execute cleaning."""
        selected = [item for item in self.items_by_id.values() if item.selected]
        if not selected:
            self.notify("No items selected to clean!", severity="warning")
            return

        def handle_confirm(confirmed: bool) -> None:
            if confirmed:
                self.notify("Executing cleanup...", severity="information")
                freed, logs = clean_items(selected, dry_run=False)
                self.notify(f"🎉 Cleaned successfully! Reclaimed {format_bytes(freed)}", severity="information", timeout=6)
                self.run_full_scan()

        self.push_screen(ConfirmCleanModal(selected, dry_run=False), handle_confirm)

    def action_refresh_scan(self) -> None:
        """Rescan all storage targets."""
        self.notify("Refreshing scan...", severity="information")
        self.run_full_scan()


def main():
    app = MacStorageOptimizerApp()
    app.run()


if __name__ == "__main__":
    main()
