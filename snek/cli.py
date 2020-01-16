import click
import os
import sys
import yaml
import logging

from sultan.api import Sultan
from snek.snek import Snek
from snek.commands import (init_command, task_run_command)
from snek.error import SnekTaskNotFound
from snek.utils import load_snekfile

logger = logging.getLogger('')
logger.setLevel(logging.ERROR)

@click.group('snek')
@click.option('-e', '--environment', default=os.environ.get('SNEK_ENV', 'dev'))
@click.pass_context
def snek(ctx, environment):
    
    ctx.obj = Snek(environment)

@snek.command()
@click.pass_context
def debug(ctx):
    """
    Prints out debug information for Snek
    """
    snek = ctx.obj
    
    # display the environment we are in
    click.secho("Environment: %s" % snek.environment, fg='green')
    
    # display the dependencies that are available in this environment
    click.secho("Dependencies:", fg='green')
    global_deps, env_deps = snek.get_dependencies()
    
    # global dependencies
    click.secho("  Dependencies Available in All Environments", fg='magenta')
    if global_deps:
        for dependency in global_deps:
            click.secho("    %s" % dependency)
    else:
        click.secho("    No Global Dependencies")
        
    # env-specific dependencies
    click.secho("  Dependencies Available in '%s'" % snek.environment, fg='magenta')
    if env_deps:
        for dependency in env_deps:
            click.secho("    %s" % dependency)
    else:
        click.secho("    No Environment-Specific Dependencies")
        
    # display the commands that are available in this environment
    click.secho("Commands:", fg='green')
    global_commands, env_commands = snek.get_commands()
    
    # global commands
    click.secho("  Global Commands:", fg='magenta')
    if global_commands:
        for command_name, commmands in global_commands.items():
            click.secho("  - %s:" % command_name, fg='magenta')
            for c in commmands:
                click.secho("    %s" % c)
    else:
        click.secho("    No Global Commands.")
            
    # env-specific commands
    click.secho("  Environment Specific Commands (%s):" % snek.environment, fg='magenta')
    if env_commands:
        for command_name, commmands in env_commands.items():
            click.secho("  - %s:" % command_name, fg='magenta')
            # click.secho(" - Commands Available in %s: %s" % (snek.environment, command_name), fg='magenta')
            for c in commmands:
                click.secho("    %s" % c)
    else:
        click.secho("No Environment-Specific Commands.")
    
    

@snek.command()
@click.option('-f', '--format', default='yaml', type=click.Choice(['json', 'yml', 'yaml']))
def init(format):
    """
    Creates a New Python project, and places a 'Snekfile' with the necessary information
    to manage a Python Project.
    """
    init_command(format)

@snek.command()
@click.argument('command')
@click.pass_context
def run(ctx, command):
    """
    Runs a task with the given 'name'.
    """
    # task_run_command(name)
    snek = ctx.obj
    snek.run_command(command)
    
