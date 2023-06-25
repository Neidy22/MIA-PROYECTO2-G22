import os
from Objects.parser import Parser
from Objects.command import Command
from Functions.server import Server


SERVER = 'server'
BUCKET = 'bucket'


class myFileSystem:

    @classmethod
    def run_file(self, fileIn):
        """
        Este método obtendrá la lista de comandos con la ayuda del Parser
        Luego ejecutará todos los comandos del archivo
        """

        command_list = Parser.run(fileIn)
        msg = ''
        for command in command_list:
            msg += self.execute_command(command)

        return msg

    @classmethod
    def run_console_input(self, input_log):
        new_command = Parser.get_command(input_log)
        msg = self.execute_command(new_command)
        return msg

    @classmethod
    def execute_command(self, command):
        msg = ''
        if command.name == 'DELETE':
            msg = self.execute_delete(command)
        msg += '\n'

        return msg

    @classmethod
    def execute_delete(self, command):
        msg = ''
        # ejecutará el comando en el servidor
        if command.parameters.get('type').lower() == SERVER:
            if command.parameters.get('name') != None:  # borrar el archivo
                msg = Server.delete(command.parameters.get('path'),
                                    command.parameters.get('name'))
            else:  # borrar la carpeta
                msg = Server.delete(command.parameters.get('path'), None)
        else:  # ejecutará el comando en el bucket
            pass

        return msg
