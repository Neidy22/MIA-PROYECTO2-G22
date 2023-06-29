import os
import shutil
import requests


class Server:

    @classmethod
    def create(self, nombre, ruta, cuerpo):
        mensaje = ""
        nombre = nombre.replace("\"", "")
        ruta = ruta.replace("\"", "")
        cuerpo = cuerpo.replace("\"", "")
        ruta = self.get_absolute_path(ruta)
        rutaAbs = ruta+nombre
        if not (os.path.exists(ruta)):  # Si las carpetas de la ruta no existen, deben crearse
            os.makedirs(ruta)

        archivo = open(rutaAbs, "w")
        archivo.write(cuerpo)
        archivo.close()
        mensaje = "Archivo creado exitosamente en la ruta: "+rutaAbs
        return mensaje

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
                shutil.rmtree(path)
                msg = 'La carpeta {} fue eliminada exitosamente \n'.format(
                    path)
            except OSError as e:
                msg = 'La carpeta {} no existe en el sistema \n {}'.format(
                    path, e)
        return msg

    @classmethod
    def copyServerServer(self, origen, destino):
        mensaje = ""
        origen = self.get_absolute_path(origen).replace("\"", "")
        destino = self.get_absolute_path(destino).replace("\"", "")

        # Si existe el origen y el destino
        if os.path.exists(origen) and os.path.exists(destino):
            # Si el origen es una carpeta, copia todos los archivos de esa carpeta
            if os.path.isdir(origen):
                archivos = os.listdir(origen)
                for archivo in archivos:
                    # copia todos los archivos al destino
                    shutil.copy(origen+archivo, destino)
                mensaje = "Se copiaron los archivos de la carpeta: " + \
                    origen + " a la carpeta: " + destino
            else:
                shutil.copy(origen, destino)  # Copia el archivo
                mensaje = "Se copió el archivo: " + origen + " a la carpeta: " + destino
        else:
            if not (os.path.exists(origen)):  # Si el origen no existe
                mensaje = "La ruta de origen no existe, por lo que no se pudo realizar la copia"
            else:
                mensaje = "La ruta destino no existe, por lo que no se pudo realizar la copia"
        return mensaje

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
    def rename(self, ruta, nuevoNombre):
        mensaje = ""
        rutaAbs = self.get_absolute_path(ruta)
        if os.path.isfile(rutaAbs):  # Si es archivo
            piezas = ruta.split("/")
            antiguo = piezas[len(piezas)-1]
            # Reemplazando el antiguo nombre con el nuevo nombre
            nuevaRuta = rutaAbs.replace(antiguo, nuevoNombre)
            # Ya hay uno con ese nombre, no se puede renombrar
            if os.path.isfile(nuevaRuta):
                mensaje = "No se puede renombrar, ya hay un archivo con ese nombre."
            else:
                os.rename(rutaAbs, nuevaRuta)  # Renombrando al archivo
                mensaje = "Se cambio exitosamente el nombre del archivo."
        elif os.path.isdir(rutaAbs):  # Si es carpeta
            piezas = ruta.split("/")
            antiguo = piezas[len(piezas)-2]
            # Reemplazando el antiguo nombre con el nuevo nombre
            nuevaRuta = rutaAbs.replace(antiguo, nuevoNombre)
            # Ya hay una carpeta con ese nombre, no se puede renombrar
            if os.path.isdir(nuevaRuta):
                mensaje = "No se puede renombrar, ya hay una carpeta con ese nombre."
            else:
                os.rename(rutaAbs, nuevaRuta)  # Renombrando la carpeta
                mensaje = "Se cambio exitosamente el nombre de la carpeta."
        else:
            mensaje = "La ruta ingresada no existe."
        return mensaje

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
            # print("La ruta server server es " + new_path)

        if os.path.exists(path_src):  # verificar que la ruta origen exista

            # Si la ruta destino no existe, la creo
            if not os.path.exists(path_dst):
                try:
                    os.makedirs(path_dst)
                except OSError as e:
                    msg = e
            # Verificando si la ruta que se creará al mover los archivos ya existe, para renombrarla

            try:
                shutil.move(path_src, path_dst, copy_function=shutil.copytree)
                msg = f"La transferencia de {path_src} a {path_dst} fue exitosa"
            except shutil.Error as e:
                msg = e

        else:
            msg = f'Error! La ruta de la que deseas transferir {path_src} no existe en el sistema'

        return msg

    @classmethod
    def recovery_server_server(self, ip, port, name):
        '''
        Copiar todos los archivos del punto de restauración en la ruta name en el server a la carpeta archivos en el server
        '''
        name = self.get_absolute_path(name)  # la ruta abosulta en el proyecto
        if ip == None and port == None:  # se trabajará sobre nuestro server
            if os.path.exists(name):
                # si la carpeta del punto de restauración existe copio el contendio de la carpeta name en la carpeta Archivos
                print("metodo copiar server server")

        else:  # se trabajará en el server del otro equipo
            pass

    @classmethod
    def backupServerServer(self, nombre_backup):
        ruta_archivos = '/home/ubuntu/Archivos/'
        ruta_backup = '/home/ubuntu/' + nombre_backup + "/"
        try:
            os.makedirs(ruta_backup)  # Creando la carpeta del Backup
            # Se copian todos los archivos de la carpeta Archivos
            shutil.copytree(ruta_archivos, ruta_backup)
            return "El backup se ha creado exitosamente en la carpeta: " + ruta_backup
        except Exception as e:
            return "Error al realizar el backup: " + str(e)

    @classmethod
    def delete_all(self):
        ruta = "/home/ubuntu/Archivos/"  # Ruta de la carpeta archivos en el server
        try:
            shutil.rmtree(ruta)
            return "Se ha vaciado la carpeta Archivos en el server."
        except Exception as e:
            print("Error al eliminar el contenido de la carpeta: " + str(e))
            return "Error al vaciar la carpeta archivos."

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
            command = {'name': name, 'type': 'server'}
            url = 'http://{ip}:{port}/file_content'.format(ip, port)
            req = requests.get(url, params=command)
            msg = req.text

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


print(Server.transfer_server_server('/"Pruebas a modificar"/',
      '/Probando/'))
'''
