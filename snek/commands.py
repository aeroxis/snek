import click
import os
import sys
import yaml

from collections import OrderedDict
from sultan.api import Sultan
from snek.error import SnekInitializationError
from snek.utils import cli_request, load_snekfile, save_snekfile


def init_command(data_format):
    """
    Creates a New Python project, and places a 'Snekfile' with the necessary information
    to manage a Python Project.
    """
    pwd = os.environ.get('PWD')
    project = load_snekfile()
    try:
        click.echo("")
        click.echo("")
        click.echo("----")
        click.echo("Snek")
        click.echo("----")
        click.echo("")
        click.echo("'snek init' will setup your project. Snek will go through a ")
        click.echo("series of questions, and based on your answers, snek will setup")
        click.echo("your python project.")
        click.echo("")
        click.echo("")
        click.echo("Once everything has been setup, run 'snek install' to setup dependencies.")
        click.echo("")
        click.echo("")
        click.echo("For more information, run 'snek --help'")
        
        project_interpretter = cli_request(
            'Which version of Python?', 
            "3.8", 
            choices=["3.8", "3.7", "3.6", "3.5"],
            show_choices=True)

        project_name = cli_request(
            'Project Name', 
            project.get('name') or os.path.basename(pwd))

        project_description = cli_request(
            'Project Description',
            project.get('description') or '')

        project_version = cli_request(
            'Project Version', 
            project.get('version') or '0.1.0')

        project_author = cli_request(
            'Project Author',
            project.get('author') or '')

        project_author_email = cli_request(
            'Project Author E-Mail',
            project.get('author_email') or '')

        project_license = cli_request(
            'Project License',
            project.get('license') or '')

        project_type = cli_request(
            'Project Type', 
            project.get('type') or 'cli', 
            choices=['cli', 'gui', 'django'], 
            show_choices=True)

        snekfile_params = OrderedDict()
        snekfile_params['name'] = project_name
        snekfile_params['description'] = project_description
        snekfile_params['version'] = project_version
        snekfile_params['author'] = project_author
        snekfile_params['author_email'] = project_author_email
        snekfile_params['license'] = project_license
        snekfile_params['type'] = project_type
        snekfile_params['interpretter'] = project_interpretter
        snekfile_params['dependencies'] = []
        snekfile_params['commands'] = {
            'test': [
                'pytest'
            ],
            'hello': [
                'echo "Hello from Snek!"',
                'cat Snekfile'
            ]
        }
        snekfile_params['env'] = {}
        snekfile_params['env']['dev'] = {
            'dependencies': ['ipython', 'ipdb', 'pytest'],
            'commands': {
                'shell': [
                    'ipython'
                ]
            }
        }

        snekfile_path = os.path.join(pwd, 'Snekfile')
        save_snekfile(snekfile_params, data_format)

        with Sultan.load(cwd=pwd) as s:
            r = s.cat(snekfile_path).run()
            for l in r.stdout:
                print(l)
        
        isOK = cli_request("Does this look OK?", 'Y', choices=['y', 'Y', 'n', 'N'])
        if isOK in ('n', 'N'):
            click.secho("Please run 'snek init' again to try again.", fg='yellow')
        
        click.secho('Your Snekfile can be found in "%s"' % snekfile_path, fg='green')

    except SnekInitializationError as e:
        
        click.secho("ERROR: %s" % e.message, fg='red')
        return


def steve_command():
    
    color = 'magenta'

    click.secho("           /^\/^\\", fg=color)
    click.secho("         _|__|  O|", fg=color)
    click.secho("\/     /~     \_/ \\", fg=color)
    click.secho(" \____|__________/  \\", fg=color)
    click.secho("        \_______      \\", fg=color)
    click.secho("                `\     \                 \\", fg=color)
    click.secho("                  |     |                  \\", fg=color)
    click.secho("                 /      /                    \\", fg=color)
    click.secho("                /     /                       \\\\", fg=color)
    click.secho("              /      /                         \ \\", fg=color)
    click.secho("             /     /                            \  \\", fg=color)
    click.secho("           /     /             _----_            \   \\", fg=color)
    click.secho("          /     /           _-~      ~-_         |   |", fg=color)
    click.secho("         (      (        _-~    _--_    ~-_     _/   |", fg=color)
    click.secho("          \      ~-____-~    _-~    ~-_    ~-_-~    /", fg=color)
    click.secho("            ~-_           _-~          ~-_       _-~", fg=color)
    click.secho("               ~--______-~                ~-___-~", fg=color)

def task_run_command(name):

    snekfile = load_snekfile().get('project', {})
    try:
        tasks = snekfile.get('tasks', {}).get(name)
        if not tasks:
            raise SnekTaskNotFound("'%s' task is not found in Snekfile" % (name))
        
        with Sultan.load() as s:
            header = "Executing '%s'" % name
            click.secho("-" * len(header), fg='cyan')
            click.secho(header, fg='cyan')
            click.secho("-" * len(header), fg='cyan')
            for task in tasks:
                s.commands = [task]
                response = s.run()
                for line in response:
                    click.secho(".\t" + line, fg='magenta')

    except Exception as e:
        click.secho("ERROR: Unable to run task '%s'" % (name), fg='red')
        click.secho("ERROR: %s" % e.message, fg='red')