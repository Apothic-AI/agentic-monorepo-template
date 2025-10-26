#!/usr/bin/env python3
"""
Claude Agents Manager - TUI for managing active and archived agents
"""

import shutil
from pathlib import Path
from typing import List

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Vertical
from textual.screen import Screen
from textual.widgets import Button, Checkbox, Footer, Header, Label, Static


# Paths
MONOREPO_ROOT = Path.cwd()
ACTIVE_AGENTS_DIR = MONOREPO_ROOT / ".claude" / "agents"
ARCHIVED_AGENTS_DIR = MONOREPO_ROOT / "archived" / ".claude" / "agents"


class AgentListScreen(Screen):
    """Screen for displaying and managing a list of agents."""

    BINDINGS = [
        Binding("a", "archive_toggle", "Archive/Activate", key_display="a"),
        Binding("up", "focus_previous", "Previous", show=False),
        Binding("down", "focus_next", "Next", show=False),
        Binding("escape", "back", "Back", key_display="esc"),
        Binding("q", "quit", "Quit", key_display="q"),
    ]

    def __init__(self, viewing_active: bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.viewing_active = viewing_active
        self.agents: List[Path] = []
        self.checkboxes: List[Checkbox] = []

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        title = "Active Agents" if self.viewing_active else "Archived Agents"
        action = 'archive' if self.viewing_active else 'activate'
        yield Header()
        yield Container(
            Label(f"[bold cyan]{title}[/bold cyan]", id="title"),
            Static(
                f"↑↓ or Tab to navigate • Space to select • 'a' to {action}",
                id="instructions",
            ),
            Vertical(id="agent-list"),
            id="main-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Load agents when screen is mounted."""
        self.load_agents()

    def load_agents(self) -> None:
        """Load agents from the appropriate directory."""
        agent_dir = ACTIVE_AGENTS_DIR if self.viewing_active else ARCHIVED_AGENTS_DIR
        self.agents = sorted(agent_dir.glob("*.md"))

        agent_list = self.query_one("#agent-list", Vertical)
        agent_list.remove_children()
        self.checkboxes = []

        if not self.agents:
            agent_list.mount(
                Label("[dim]No agents found[/dim]", classes="no-agents")
            )
        else:
            for agent_path in self.agents:
                # Get file size
                size_kb = agent_path.stat().st_size / 1024
                label = f"{agent_path.name} ({size_kb:.1f}k)"
                checkbox = Checkbox(label, False)
                self.checkboxes.append(checkbox)
                agent_list.mount(checkbox)

            # Auto-focus the first checkbox
            if self.checkboxes:
                self.checkboxes[0].focus()

    def action_archive_toggle(self) -> None:
        """Archive or activate selected agents."""
        selected_indices = [
            i for i, cb in enumerate(self.checkboxes) if cb.value
        ]

        if not selected_indices:
            self.notify("No agents selected", severity="warning")
            return

        dest_dir = ARCHIVED_AGENTS_DIR if self.viewing_active else ACTIVE_AGENTS_DIR

        # Ensure destination directory exists
        dest_dir.mkdir(parents=True, exist_ok=True)

        moved_count = 0
        for idx in selected_indices:
            agent_path = self.agents[idx]
            dest_path = dest_dir / agent_path.name

            try:
                shutil.move(str(agent_path), str(dest_path))
                moved_count += 1
            except Exception as e:
                self.notify(
                    f"Error moving {agent_path.name}: {e}", severity="error"
                )

        action = "archived" if self.viewing_active else "activated"
        self.notify(f"{moved_count} agent(s) {action}", severity="information")

        # Reload the list
        self.load_agents()

    def action_back(self) -> None:
        """Return to main menu."""
        self.app.pop_screen()

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_focus_previous(self) -> None:
        """Focus the previous checkbox."""
        if not self.checkboxes:
            return

        # Find currently focused checkbox
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.has_focus:
                # Move to previous (wrap to last if at first)
                prev_index = (i - 1) % len(self.checkboxes)
                self.checkboxes[prev_index].focus()
                return

    def action_focus_next(self) -> None:
        """Focus the next checkbox."""
        if not self.checkboxes:
            return

        # Find currently focused checkbox
        for i, checkbox in enumerate(self.checkboxes):
            if checkbox.has_focus:
                # Move to next (wrap to first if at last)
                next_index = (i + 1) % len(self.checkboxes)
                self.checkboxes[next_index].focus()
                return


class MainMenuScreen(Screen):
    """Main menu screen for selecting between active and archived agents."""

    BINDINGS = [
        Binding("up", "focus_previous", "Previous", show=False),
        Binding("down", "focus_next", "Next", show=False),
        Binding("q", "quit", "Quit"),
    ]

    CSS = """
    MainMenuScreen {
        align: center middle;
    }

    #menu-container {
        width: 60;
        height: auto;
        border: solid cyan;
        padding: 2;
    }

    #title {
        width: 100%;
        text-align: center;
        margin-bottom: 2;
    }

    .menu-button {
        width: 100%;
        margin: 1;
    }

    .menu-button:focus {
        border: tall $accent;
    }
    """

    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        yield Container(
            Label("[bold cyan]Claude Agents Manager[/bold cyan]", id="title"),
            Button("Active Agents", id="active-btn", classes="menu-button"),
            Button("Archived Agents", id="archived-btn", classes="menu-button"),
            id="menu-container",
        )
        yield Footer()

    def on_mount(self) -> None:
        """Focus first button when screen loads."""
        self.query_one("#active-btn", Button).focus()

    @on(Button.Pressed, "#active-btn")
    def show_active_agents(self) -> None:
        """Show active agents screen."""
        self.app.push_screen(AgentListScreen(viewing_active=True))

    @on(Button.Pressed, "#archived-btn")
    def show_archived_agents(self) -> None:
        """Show archived agents screen."""
        self.app.push_screen(AgentListScreen(viewing_active=False))

    def action_quit(self) -> None:
        """Quit the application."""
        self.app.exit()

    def action_focus_previous(self) -> None:
        """Focus the previous button."""
        self.focus_previous()

    def action_focus_next(self) -> None:
        """Focus the next button."""
        self.focus_next()


class ClaudeAgentsApp(App):
    """Main application for managing Claude agents."""

    def on_mount(self) -> None:
        """Initialize app and ensure required directories exist."""
        # Create archived agents directory if it doesn't exist
        ARCHIVED_AGENTS_DIR.mkdir(parents=True, exist_ok=True)
        # Show main menu
        self.push_screen(MainMenuScreen())

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    #title {
        width: 100%;
        text-align: center;
        margin-bottom: 1;
    }

    #instructions {
        width: 100%;
        text-align: center;
        margin-bottom: 2;
        color: $text-muted;
    }

    #agent-list {
        width: 100%;
        height: 1fr;
        overflow-y: auto;
    }

    Checkbox {
        margin: 0 2;
        background: $surface;
    }

    Checkbox:focus {
        background: $accent 20%;
        border-left: thick $accent;
    }

    Checkbox:hover {
        background: $panel 50%;
    }

    .no-agents {
        width: 100%;
        text-align: center;
        margin-top: 4;
    }
    """

    TITLE = "Claude Agents Manager"


def main():
    """Run the application."""
    app = ClaudeAgentsApp()
    app.run()


if __name__ == "__main__":
    main()
