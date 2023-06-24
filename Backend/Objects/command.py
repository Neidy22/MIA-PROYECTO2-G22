class Command:

    def __init__(self, name, parameters):
        """
            La función inicializa un nuevo comando.

            Argumentos
            name (string)
            parameters (diccionario)
        """
        self.name = name
        self.parameters = parameters
        self.line = ''

    def setLine(self, line):
        self.line = line
