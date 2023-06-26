from Objects.command import Command


class Parser:

    @classmethod
    def run(self, my_file):
        """
            Iterará línea por línea el contenido del archivo para extraer
            los comandos

            Argumentos:
            my_file(File)

            Retorna una lista de comandos cada uno con nombre y su diccionario de parámetros

        """
        command_list = list()

        # lines = my_file.readlines()
        lines = my_file.split("\n")

        # Obtener los comandos
        for line in lines:
            command = self.get_command(line)
            command_list.append(command)

        return command_list

    @classmethod
    def get_command(self, line):
        line = line.rstrip()  # Elimino el salto de línea
        # Separo los elementos del comando
        actual_command = line.split(" -")
        # Obtengo el nombre del comando
        command_name = actual_command[0].upper()
        # actualizo a una sublista en la que almaceno solo los parámetros
        actual_command = actual_command[1:]
        # genero el diccionario en el que se almacenarán los parámetros del comando
        command_parameters = dict()

        for parameter in actual_command:
            actual_parameter = parameter.split('->')
            command_parameters[actual_parameter[0].lower(
            )] = actual_parameter[1]

        command = Command(command_name, command_parameters)
        command.setLine(line)

        return command
