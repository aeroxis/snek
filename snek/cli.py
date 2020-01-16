import click
import os
import sys
import yaml
import logging

from sultan.api import Sultan
from snek.commands import (init_command, steve_command, task_run_command)
from snek.error import SnekTaskNotFound
from snek.utils import load_snekfile

logger = logging.getLogger('')
logger.setLevel(logging.ERROR)

@click.group('snek')
def snek():
    pass

@snek.command()
def steve():
    """
    Call out steve for a show!
    """
    steve_command()

@snek.command()
@click.option('-f', '--format', default='yaml', type=click.Choice(['json', 'yml', 'yaml']))
def init(format):
    """
    Creates a New Python project, and places a 'Snekfile' with the necessary information
    to manage a Python Project.
    """
    init_command(format)

@snek.command()
@click.argument('name')
def run(name):
    """
    Runs a task with the given 'name'.
    """
    task_run_command(name)