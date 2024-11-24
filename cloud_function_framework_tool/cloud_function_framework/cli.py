import click
from cloud_function_framework.project_setup import setup_project


@click.group(help="CLI Tool for Google Cloud Function Setup.")
def cli():
    pass


@cli.group(help="Commands for initializing and managing library projects.")
def library():
    pass

@library.command(help="Bootstrap a new project structure in the current directory.")
@click.argument("project_name")
def bootstrap(project_name):
    """Initialize a new project structure."""
    click.echo(f"Initializing project: {project_name}")
    setup_project(project_name)


if __name__ == "__main__":
    cli()
