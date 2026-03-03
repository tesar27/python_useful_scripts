import typer
from image_compression.compress_image import run as compress_run

app = typer.Typer(help="Collection of utility scripts.")

@app.command("image-compression")
def image_compression(
    source: str = typer.Option(..., help="Source folder path"),
    output: str = typer.Option("output", help="Output folder path"),
    quality: int = typer.Option(2, min=1, max=10, help="Quality level 1-10")
):
    """Compress images in a folder and create a PDF."""
    compress_run(source, output, quality)

@app.command("interactive")
def interactive():
    """Start interactive CLI mode."""
    # your interactive logic here
    typer.echo("Starting interactive mode...")

@app.command("version")
def version():
    """Show version."""
    typer.echo("v1.0.0")

if __name__ == "__main__":
    app()