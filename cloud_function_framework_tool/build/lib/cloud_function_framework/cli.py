import click
from cloud_function_framework.project_setup import setup_project


@click.group()
def cli():
    """CLI Tool for Google Cloud Function Setup."""
    pass


@cli.command()
@click.argument("project_name")
def bootstrap(project_name):
    """Initialize a new project structure."""
    click.echo(f"Initializing project: {project_name}")
    setup_project(project_name)


if __name__ == "__main__":
    cli()
