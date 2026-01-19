import os
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.logging import RichHandler
import logging

from .core import Exporter, GroupMeClient
from .analysis import download_images as dl_images

app = typer.Typer(help="GroupMe Archive: A modern CLI for archiving your GroupMe chats.")
console = Console()

def get_client(token: Optional[str]) -> GroupMeClient:
    """Initialize GroupMe client from token or file/env."""
    if not token:
        # Try environment variable
        token = os.getenv("GROUPME_ACCESS_TOKEN")
        
    if not token:
        # Try token.txt
        token_file = Path("token.txt")
        if token_file.exists():
            token = token_file.read_text().splitlines()[0].strip()
            
    if not token:
        console.print("[red]Error: Access token not found.[/red]")
        console.print("Please provide --token, set GROUPME_ACCESS_TOKEN, or create token.txt")
        raise typer.Exit(code=1)
        
    return GroupMeClient(token)

def setup_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

@app.command()
def list_groups(
    token: Optional[str] = typer.Option(None, help="GroupMe Access Token"),
    output: Path = typer.Option(Path("archives/groups_list.txt"), help="File to save the list"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show debug logs")
):
    """List all groups and their creation timestamps."""
    setup_logging(verbose)
    client = get_client(token)
    exporter = Exporter(client)
    
    with console.status("[bold green]Fetching groups..."):
        groups = exporter.list_groups_summary()
        exporter.export_group_listing(output)
    
    table = Table(title="GroupMe Groups")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="green")
    table.add_column("Created At", style="magenta")
    
    for g in groups:
        table.add_row(g['id'], g['name'], g['created_at'])
        
    console.print(table)
    console.print(f"\n[bold green]Successfully exported group listing to {output}[/bold green]")

@app.command()
def archive(
    group_id: Optional[str] = typer.Option(None, help="ID of the group to archive. If omitted, lists groups first."),
    token: Optional[str] = typer.Option(None, help="GroupMe Access Token"),
    output_dir: Optional[Path] = typer.Option(None, help="Directory to save the archive files. Defaults to archives/[name]_[id]"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show debug logs")
):
    """Archive all messages from a specific group."""
    setup_logging(verbose)
    client = get_client(token)
    exporter = Exporter(client)
    
    if not group_id:
        # Prompt user with list if no ID provided
        with console.status("[bold green]Fetching groups..."):
            groups = client.list_groups()
        
        console.print("\n[bold]Select a group ID to archive:[/bold]")
        for g in groups:
            console.print(f"  [cyan]{g['group_id']}[/cyan] : {g['name']}")
        return

    if not output_dir:
        group_data = client.get_group(group_id)
        safe_name = exporter._safe_name(group_data['name'])
        output_dir = Path("archives") / f"{safe_name}_{group_id}"

    with console.status(f"[bold green]Archiving group {group_id} to {output_dir}..."):
        exporter.archive_group(group_id, output_dir)
    
    console.print(f"[bold green]Archive complete! Files saved to {output_dir}[/bold green]")

@app.command()
def download_images(
    group_subdir: str = typer.Argument(..., help="Subdirectory name in archives/ (e.g. Tennis_65850956)"),
    csv_path: Optional[Path] = typer.Option(None, help="Path to the archived messages CSV"),
    output_dir: Optional[Path] = typer.Option(None, help="Directory to save images"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show debug logs")
):
    """Download images from an existing archive CSV."""
    setup_logging(verbose)
    
    if not csv_path:
        csv_path = Path("archives") / group_subdir / "historic_messages.csv"
    
    if not output_dir:
        output_dir = Path("archives") / group_subdir
    
    with console.status(f"[bold green]Downloading images from {csv_path} to {output_dir}..."):
        dl_images(group_subdir, csv_path, output_dir)
    console.print("[bold green]Image download complete.[/bold green]")

if __name__ == "__main__":
    app()
