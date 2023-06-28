from Objects.parser import Parser
from Functions.server import Server
from Functions.bucket import Bucket


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
        if command.name == 'CREATE':
            msg = self.execute_create(command)
        elif command.name == 'DELETE':
            msg = self.execute_delete(command)
        elif command.name == 'COPY':
            msg = self.execute_copy(command)
        elif command.name == 'TRANSFER':
            msg = self.execute_transfer(command)
        elif command.name == 'RENAME':
            msg = self.execute_rename(command)
        elif command.name == 'MODIFY':
            msg = self.execute_modify(command)
        elif command.name == 'BACKUP':
            msg = self.execute_backup(command)
        elif command.name == 'RECOVERY':
            msg = self.execute_recovery(command)
        elif command.name == 'DELETE_ALL':
            msg = self.execute_delete_all(command)
        elif command.name == 'OPEN':
            msg = self.execute_open(command)

        msg += '\n'

        return msg

    @classmethod
    def execute_create(self, command):
        msg = ''
        # ejecutará el comando en el servidor
        if command.parameters.get('type').lower() == SERVER:

            msg = Server.delete(command.parameters.get(
                'path'), command.parameters.get('name'))

        else:  # ejecutará el comando en el bucket
            msg = Bucket.delete(command.parameters.get(
                'path'), command.parameters.get('name'))

        return msg

    @classmethod
    def execute_delete(self, command):
        msg = ''
        # ejecutará el comando en el servidor
        if command.parameters.get('type').lower() == SERVER:

            msg = Server.delete(command.parameters.get(
                'path'), command.parameters.get('name'))

        else:  # ejecutará el comando en el bucket
            msg = Bucket.delete(command.parameters.get(
                'path'), command.parameters.get('name'))

        return msg

    @classmethod
    def execute_copy(self, command):
        msg = ''
        return msg

    @classmethod
    def execute_transfer(self, command):
        msg = ''
        if command.parameters.get('type_from').lower() == SERVER:
            # transferencia server-server
            if command.parameters.get('type_to').lower() == SERVER:
                msg = Server.transfer_server_server(
                    command.parameters.get('from'), command.parameters.get('to'))
            else:  # transferencia server-bucket
                msg = Bucket.transfer_server_bucket(
                    command.parameters.get('from'), command.parameters.get('to'))
        else:
            # transferencia bucket-server
            if command.parameters.get('type_to').lower() == SERVER:
                msg = Bucket.transfer_bucket_server(
                    command.parameters.get('from'), command.parameters.get('to'))
            else:  # transferencia bucket-bucket
                msg = Bucket.transfer_bucket_bucket(
                    command.parameters.get('from'), command.parameters.get('to'))

        return msg

    @classmethod
    def execute_rename(self, command):
        msg = ''
        return msg

    @classmethod
    def execute_modify(self, command):
        msg = ''
        if command.parameters.get('type').lower() == SERVER:
            msg = Server.modify(command.parameters.get(
                'path'), command.parameters.get('body'))
        else:
            msg = Bucket.modify(command.parameters.get(
                'path'), command.parameters.get('body'))
        return msg

    @classmethod
    def execute_backup(self, command):
        msg = ''
        return msg

    @classmethod
    def execute_recovery(self, command):
        msg = ''
        # type_from indica si el recovery se recuperará desde nuestro server o nuestro bucket
        # type_to indica si el recovery se restablecerá en un servidor o en un bucket
        if command.parameters.get('type_from').lower() == SERVER:
            # recovery server-server
            if command.parameters.get('type_to').lower() == SERVER:
                msg = Server.recovery_server_server(command.parameters.get(
                    'ip'), command.parameters.get('port'), command.parameters.get('name'))
            else:  # recovery server-bucket
                msg = Bucket.recovery_server_bucket(command.parameters.get(
                    'ip'), command.parameters.get('port'), command.parameters.get('name'))
        else:
            # recovery bucket-server
            if command.parameters.get('type_to').lower() == SERVER:
                msg = Bucket.recovery_bucket_server(command.parameters.get(
                    'ip'), command.parameters.get('port'), command.parameters.get('name'))
            else:  # recovery bucket-bucket
                msg = Bucket.recovery_bucket_bucket(command.parameters.get(
                    'ip'), command.parameters.get('port'), command.parameters.get('name'))

        return msg

    @classmethod
    def execute_delete_all(self, command):
        msg = ''
        return msg

    @classmethod
    def execute_open(self, command):
        msg = ''
        if command.parameters.get('type').lower() == SERVER:
            msg = Server.open(command.parameters.get('ip'), command.parameters.get(
                'port'), command.parameters.get('name'))
        else:
            msg = Bucket.open(command.parameters.get('ip'), command.parameters.get(
                'port'), command.parameters.get('name'))

        return msg

    @classmethod
    def send_file_content(self, type, name):
        msg = ''
        if type == SERVER:
            msg = Server.open(None, None, name)
        else:
            msg = Bucket.open(None, None, name)
        return msg


'''
content = ''
with open('..\Archivos\prueba1.mia', 'r') as file:
    content = file.read()

mensaje = myFileSystem.run_file(content)
print(mensaje)

'''
