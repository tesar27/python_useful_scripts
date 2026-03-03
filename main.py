import typer
import inspect
from image_compression.compress_image import run as compress_run

app = typer.Typer(help="Collection of utility scripts.", no_args_is_help=False)

# Registry mirrors interactive.py — keep in sync when adding modules
MODULES = {
    "image-compression": compress_run,
}

@app.callback(invoke_without_command=True)
def default(ctx: typer.Context):
    """Show info about this CLI and all available modules."""
    if ctx.invoked_subcommand is not None:
        return

    typer.echo("\n  Scripts CLI — Collection of utility scripts.")
    typer.echo("  Usage: python main.py <command> [OPTIONS]\n")
    typer.echo("  Available commands:")
    typer.echo("    image-compression   Compress images in a folder and create a PDF.")
    typer.echo("    interactive         Start interactive CLI mode.")
    typer.echo("    version             Show version.\n")

    typer.echo("  Module arguments:")
    for module_name, run_func in MODULES.items():
        typer.echo(f"\n  [{module_name}]")
        sig = inspect.signature(run_func)
        hints = inspect.get_annotations(run_func)
        for name, param in sig.parameters.items():
            required = param.default is inspect.Parameter.empty
            arg_type = hints.get(name, str).__name__
            default_val = "required" if required else f"default: {param.default}"
            typer.echo(f"    --{name}  ({arg_type}, {default_val})")

    typer.echo("\n  Run 'python main.py --help' for full usage details.\n")

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
    from cli.interactive import interactive_cli
    interactive_cli()

@app.command("version")
def version():
    """Show version."""
    typer.echo("v1.0.0")

if __name__ == "__main__":
    app()