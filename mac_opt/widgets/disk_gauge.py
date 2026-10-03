from textual.widgets import Static
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from mac_opt.models import DiskStats


class DiskGaugeWidget(Static):
    """Widget displaying a visual APFS container disk usage gauge."""

    def __init__(self, stats: DiskStats, **kwargs):
        super().__init__(**kwargs)
        self.stats = stats

    def update_stats(self, stats: DiskStats) -> None:
        self.stats = stats
        self.refresh()

    def render(self) -> Panel:
        s = self.stats
        pct = s.percent_used
        bar_len = 36
        filled = int((pct / 100.0) * bar_len)
        empty = bar_len - filled

        # Color based on capacity
        if pct < 50:
            bar_color = "green"
            status_text = "[bold green]Healthy[/bold green]"
        elif pct < 75:
            bar_color = "yellow"
            status_text = "[bold yellow]Moderate[/bold yellow]"
        else:
            bar_color = "red"
            status_text = "[bold red]Critical Warning[/bold red]"

        bar = f"[{bar_color}]{'█' * filled}[/{bar_color}][dim]{'░' * empty}[/dim]"

        t = Table.grid(expand=True)
        t.add_column(ratio=3)
        t.add_column(ratio=2, justify="right")

        t.add_row(
            Text.from_markup(f"[bold white]{s.container_name}[/bold white]  {bar} [bold cyan]{pct:.1f}%[/bold cyan]"),
            Text.from_markup(f"Free: [bold green]{s.free_human}[/bold green] | Used: [bold yellow]{s.used_human}[/bold yellow] | Total: [bold]{s.total_human}[/bold]")
        )

        return Panel(t, title="[bold cyan]💾 APFS Storage Status[/bold cyan]", border_style="cyan")
