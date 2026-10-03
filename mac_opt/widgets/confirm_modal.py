from typing import List
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Static
from textual.containers import Vertical, Horizontal
from mac_opt.models import CleanableItem, format_bytes, RiskLevel


class ConfirmCleanModal(ModalScreen[bool]):
    """Modal dialog to confirm deletions with a summary of reclaimable space."""

    def __init__(self, selected_items: List[CleanableItem], dry_run: bool = False):
        super().__init__()
        self.selected_items = selected_items
        self.dry_run = dry_run

    def compose(self) -> ComposeResult:
        total_size = sum(item.size_bytes for item in self.selected_items)
        has_review = any(item.risk == RiskLevel.REVIEW for item in self.selected_items)
        has_caution = any(item.risk == RiskLevel.CAUTION for item in self.selected_items)

        title = "🔍 Dry Run Preview" if self.dry_run else "⚠️ Confirm Deletion"
        btn_label = "Proceed" if self.dry_run else "Confirm & Clean"
        btn_variant = "primary" if self.dry_run else "error"

        summary_lines = [
            f"[bold cyan]{title}[/bold cyan]\n",
            f"Items selected: [bold yellow]{len(self.selected_items)}[/bold yellow]",
            f"Space to reclaim: [bold green]{format_bytes(total_size)}[/bold green]\n",
        ]

        if not self.dry_run:
            if has_caution:
                summary_lines.append("[bold red]🚨 Warning: Includes CAUTION items. Please verify paths carefully.[/bold red]")
            elif has_review:
                summary_lines.append("[bold yellow]⚠️ Note: Includes items that may require re-downloading or profile data.[/bold yellow]")

        summary_lines.append("\n[bold]Selected Targets:[/bold]")
        for item in self.selected_items[:8]:
            summary_lines.append(f"  • {item.risk.badge} {item.title} ([bold]{item.size_human}[/bold])")
        if len(self.selected_items) > 8:
            summary_lines.append(f"  [dim]... and {len(self.selected_items) - 8} more items[/dim]")

        with Vertical(id="modal_dialog"):
            yield Static("\n".join(summary_lines), id="modal_content")
            with Horizontal(id="modal_buttons"):
                yield Button(btn_label, variant=btn_variant, id="btn_confirm")
                yield Button("Cancel", variant="default", id="btn_cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn_confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)
