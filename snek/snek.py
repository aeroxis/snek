import click
import subprocess

from snek import utils
from sultan.api import Sultan

class Snek(object):
    
    def __init__(self, environment):
        super().__init__()
        self.environment = environment
        self.snekfile = utils.load_snekfile()
    
    def get_dependencies(self):
        
        env = self.environment
        global_dependencies = self.snekfile.get('dependencies', [])
        env_dependencies = self.snekfile.get('env', {}).get(env, {}).get('dependencies', [])
        return global_dependencies, env_dependencies
        
    def get_commands(self):
        
        env = self.environment
        global_commands = self.snekfile.get('commands', {})
        env_commands = self.snekfile.get('env', {}).get(env, {}).get('commands', {})
        return global_commands, env_commands
    
    def run_command(self, command):
        
        env = self.environment
        global_cmds, env_cmds = self.get_commands()
        try:
            commands_to_run = {}
            commands_to_run.update(global_cmds)
            commands_to_run.update(env_cmds)
            commands = commands_to_run[command]
            for cmd in commands:
                
                click.secho(cmd, fg='green')
                # with Sultan.load() as s:
                #     # cmd = "ls -lah "
                #     # s.commands = cmd.split(" ")
                #     # r = s.run(quiet=True)
                #     r = s.ls("-lah").run()
                #     for line in r.stdout:
                #         click.secho("[stdout] %s " % line, fg='magenta')
                #     print("--")
                #     for line in r.stderr:
                #         click.secho("[stderr] %s " % line, fg='red')
                
                # run the command
                process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
                output, error = process.communicate()
                
                # show the output if the process gave an output
                if output:
                    for line in output.decode("utf-8").split("\n"):
                        click.secho("\t %s" % line, fg='magenta')
                        
                # show the error if there were some errors
                if error:
                    for line in error.decode("utf-8").split("\n"):
                        click.secho("\t %s" % line, fg='red')
                    
        except KeyError as e:
            click.secho('Command "%s" does not exist in your Snekfile. Please add a new command by calling "snek add command"' % command)
            return