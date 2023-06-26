import os
import shutil


class Server:

    @classmethod
    def delete(self, path, name):

        path = self.get_absolute_path(path)
        msg = ''

        if name != None:  # remover el archivo
            name = name.replace('\"', "")

            if os.path.exists(path+name):
                os.remove(path+name)
                msg = 'Se elimino el archivo {} exitosamente \n'.format(name)
            else:
                msg = 'El archivo {} no existe en la ruta {} \n'.format(
                    name, path)

        else:  # remover la carpeta
            try:
                os.rmdir(path)
                msg = 'La carpeta {} fue eliminada exitosamente \n'.format(
                    name)
            except OSError as e:
                msg = 'La carpeta {} no existe en el sistema \n'.format(path)
        return msg

    @classmethod
    def modify(self, path, body):

        path = self.get_absolute_path(path)
        body = body.replace('\"', "")

        msg = ''
        if os.path.exists(path):
            my_file = open(path, "w")
            my_file.flush()
            my_file.close()

            my_file = open(path, "w")
            my_file.write(body)
            my_file.close()
            msg = 'Se modificó el contenido del archivo ubicado en la ruta {}'.format(
                path)
        else:
            msg = 'La ruta del archivo {} no existe en el server'.format(path)

        return msg

    @classmethod
    def transfer_server_server(self, from_path, to_path):

        msg = ''
        from_path = from_path.strip("\"")
        to_path = to_path.strip("\"")

        path_src = self.get_absolute_path(from_path)
        path_dst = self.get_absolute_path(to_path)

        new_path = ''
        if (from_path[0] == '/'):
            from_path = from_path[1:]
            new_path = f'{to_path}{from_path}'
            new_path = self.get_absolute_path(new_path)
            print("La ruta server server es " + new_path)

        if os.path.exists(path_src):  # verificar que la ruta origen exista

            # Si la ruta destino no existe, la creo
            if not os.path.exists(path_dst):
                try:
                    os.makedirs(path_dst)
                except OSError as e:
                    msg = e
            # Verificando si la ruta que se creará al mover los archivos ya existe, para renombrarla

            try:
                shutil.move(path_src, path_dst)
                msg = f"La transferencia de {path_src} a {path_dst} fue exitosa"
            except shutil.Error as e:
                msg = e

        else:
            msg = f'Error! La ruta de la que deseas transferir {path_src} no existe en el sistema'

        return msg

    @classmethod
    def recovery_server_server(self, ip, port, name):

        name = self.get_absolute_path(name)  # la ruta abosulta en el proyecto

    @classmethod
    def open(self, ip, port, name):

        msg = ''
        name = self.get_absolute_path(name)
        if ip == None and port == None:  # se abre desde el servidor propio

            if os.path.exists(name):
                # realizar la restauración de la copia de seguridad

                # abrir para obtener el contenido del archivo
                with open(name, 'r') as file:
                    msg = file.read()

            else:
                msg = f"El archivo en la ruta {name} no existe!"

        else:  # se abre en nuestro servidor desde otro servidor o bucket
            pass

        return msg

    @classmethod
    def get_absolute_path(self, path):
        path_a = path.replace('\"', "")
        # path_a = path_a.replace('/', '\\')
        abs_path = f'../../Archivos{path_a}'
        return abs_path


'''
print(Server.modify('/"Pruebas a modificar"/modificar.txt',
      "este es el nuevo contenido modificado"))
print(Server.open(None, None, '/"Pruebas a modificar"/abrir.txt'))
print(Server.transfer_server_server('/"Pruebas a modificar"/transferir.txt',
      '/"Pruebas a borrar"/borrar2'))
print(Server.delete('/"Pruebas a borrar"/borrar2/', "borrado 2.txt"))

'''
