import requests
import typer
import sys
from rich.console import Console
from rich.progress import Progress
from tqdm import tqdm

console = Console()
app = typer.Typer()

BASE_URL = "https://fastapi-dependency-api.azurewebsites.net"

@app.command()
def upload(file: str):
    """Upload a requirements.txt file to the server."""
    console.print(f"📤 Uploading [bold cyan]{file}[/]...", style="bold yellow")
    with open(file, "rb") as f:
        response = requests.post(f"{BASE_URL}/upload/", files={"file": f})
    
    if response.status_code == 200:
        console.print("✅ [green]Upload successful![/]", style="bold")
    else:
        console.print(f"❌ [red]Error: {response.text}[/]")

@app.command()
def list_dependencies(file: str):
    """List dependencies from a requirements.txt file."""
    console.print(f"📜 Fetching dependencies from [bold cyan]{file}[/]...", style="bold yellow")
    response = requests.get(f"{BASE_URL}/dependencies/?filename={file}")
    
    if response.status_code == 200:
        deps = response.json().get("dependencies", [])
        for dep in deps:
            console.print(f"🔹 {dep}", style="bold green")
    else:
        console.print(f"❌ [red]Error: {response.text}[/]")

@app.command()
def install(file: str):
    """Install dependencies with a progress bar."""
    console.print(f"⚙️ Installing dependencies from [bold cyan]{file}[/]...", style="bold yellow")
    response = requests.post(f"{BASE_URL}/install/?filename={file}")
    
    if response.status_code == 200:
        details = response.json().get("details", [])
        with Progress() as progress:
            task = progress.add_task("Installing...", total=len(details))
            for dep in tqdm(details, desc="Processing", unit="pkg"):
                console.print(f"✅ {dep}", style="bold green")
                progress.update(task, advance=1)
    else:
        console.print(f"❌ [red]Error: {response.text}[/]")

if __name__ == "__main__":
    app()
