import click
import os
import simplejson as json
import yaml
import yamlordereddictloader

from six.moves import input
from snek.error import SnekInitializationError

def cli_request(question, answer=None, choices=None, show_choices=False, cast=None, attempt=0):
    """
    Asks the question 'question' and if an answer is provided, it is returned.
    If no answer is provided, the 'answer' is returned. The optional 
    parameter 'cast' is used to cast the provided answer from the user back.
    """

    # if the developer did something wacky, prompt them now.
    # hopefully they will see it before their code goes into production
    if choices:
        if answer not in choices:
            raise ValueError("Hey Developer, your answer is not in your choices. Fix this.")
    
    # if this is the user's 3rd attempt, let's stop it and throw an error
    if attempt:
        if attempt == 3:
            raise SnekInitializationError("Invalid Value for question '%s'" % question)
        else:
            click.secho("Invalid Response. Try Again!", fg='red')
    
    # determine how we'll format choices and answers
    if choices and answer:
        if show_choices:
            options = " (choices=%s: default=%s): " % (','.join([str(c) for c in choices]), answer)
        else:
            options = " (default=%s): " % (answer)
    elif not choices and answer:
        options = " (default=%s): " % (answer)
    else:
        options = ": "
    
    q_len = 80
    if attempt==0:
        click.secho("=" * q_len, fg='green')
    click.secho(question + options, fg='green')
    response = cast(input(":: ")) if cast else input("?: ")
    if (response == '') and answer:
        response = answer

    # ensure that the user's input is a valid one if the choices are provided.
    if choices:
        if response not in choices:
            response = cli_request(question, answer=answer, choices=choices, show_choices=False, cast=cast, attempt=attempt+1)
            
    return response
    
def load_snekfile():

    pwd = os.environ.get('PWD')
    snekfile_path = os.path.join(pwd, 'Snekfile')
    if os.path.exists(snekfile_path):

        with open(snekfile_path, 'r') as f:
            try:
                return yaml.load(f, Loader=yamlordereddictloader.Loader)
            except yaml.YAMLError as e:
                return {}
    else:
        return {}

def save_snekfile(data, format):

    pwd = os.environ.get('PWD')
    snekfile_path = os.path.join(pwd, 'Snekfile')

    if format in ['yml', 'yaml']:
        with open(snekfile_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, Dumper=yamlordereddictloader.Dumper)
    else:
        with open(snekfile_path, 'w') as f:
            json.dump(data, f, indent=4)