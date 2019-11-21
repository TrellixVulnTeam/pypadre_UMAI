"""
Command Line Interface for PADRE.

"""
import os

import click
#################################
####### PROJECT FUNCTIONS ##########
#################################
from click_shell import make_click_shell

from pypadre.cli.experiment import experiment_cli
from pypadre.core.model.project import Project
from pypadre.core.validation.json_schema import JsonSchemaRequiredHandler
from pypadre.pod.app.project.project_app import ProjectApp


@click.group(name="project")
@click.pass_context
def project(ctx):
    pass


def _get_app(ctx) -> ProjectApp:
    return ctx.obj["pypadre-app"].projects


def _print_table(ctx, *args, **kwargs):
    ctx.obj["pypadre-app"].print_tables(Project, *args, **kwargs)


@project.command(name="list")
@click.option('--offset', '-o', default=0, help='start number of the dataset')
@click.option('--limit', '-l', default=100, help='Number of datasets to retrieve')
@click.option('--search', '-s', default=None,
              help='search string')
@click.option('--column', '-c', help="Column to print", default=None, multiple=True)
@click.pass_context
def list(ctx, search, offset, limit, column):
    """
    List projects defined in the padre environment
    """
    # List all the projects that are currently saved
    _print_table(ctx, _get_app(ctx).list(search=search, offset=offset, size=limit), columns=column)


@project.command(name="get")
@click.argument('id', type=click.STRING)
@click.pass_context
def get(ctx, id):
    try:
        found = _get_app(ctx).get(id)
        if len(found) == 0:
            click.echo(click.style(str("No project found for id: " + id), fg="red"))
        elif len(found) >= 2:
            click.echo(click.style(str("Multiple projects found for id: " + id), fg="red"))
            _print_table(ctx, found)
        else:
            ctx.obj["pypadre-app"].print(found.pop())
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


@project.command(name="create")
@click.option('--name', '-n', default="CI created project", help='Name of the project')
@click.pass_context
def create(ctx, name):
    """
    Create a new project
    """
    # Create a new project
    def get_value(obj, e, options):
        return click.prompt(e.message + '. Please enter a value', type=str)

    app = _get_app(ctx)
    try:
        p = app.create(name=name, handlers=[JsonSchemaRequiredHandler(validator="required", get_value=get_value)])
        app.put(p)
    except Exception as e:
        click.echo(click.style(str(e), fg="red"))


@click.group(name="select", invoke_without_command=True)
@click.argument('name', type=click.STRING)
@click.pass_context
def select(ctx, id):
    """
    Select a project as active
    """
    # Set as active project
    projects = _get_app(ctx).list({"id": id})
    if len(projects) == 0:
        print("Project {0} not found!".format(id))
        return -1
    if len(projects) > 1:
        print("Multiple matching projects found!")
        _print_table(ctx, projects)
        return -1
    s = make_click_shell(ctx, prompt='pypadre > pro: ' + id + ' > ', intro='Selecting project ' + name, hist_file=os.path.join(os.path.expanduser('~'), '.click-pypadre-history'))
    ctx.obj['project'] = projects.pop(0)
    s.cmdloop()
    ctx.obj['project'] = None


project.add_command(select)
select.add_command(experiment_cli.experiment)
