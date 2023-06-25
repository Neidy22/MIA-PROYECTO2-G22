import os
import boto3


class Server:

    @classmethod
    def create(self, ruta, nombre, contenido):
        s3 = boto3.client('s3') #Conectandome a s3
        s3.put_object(Body=contenido, Bucket='mi-bucket', Key=ruta+nombre) #Creando el archivo
        
    @classmethod
    def delete(self, path, name):
        path = self.get_absolute_path(path)
        msg = ''

        if name != None:  # remover el archivo
            name = name.replace('\"', "")

            if os.path.exists(path+name):
                os.remove(path+name)
                msg = f'Se elimino el archivo {name} exitosamente \n'
            else:
                msg = f'El archivo {name} no existe en la ruta {path} \n'

        else:  # remover la carpeta
            try:
                os.rmdir(path)
                msg = f'La carpeta {path} fue eliminada exitosamente \n'
            except OSError as e:
                msg = f'La carpeta {path} no existe en el sistema \n'
        return msg

    @classmethod
    def get_absolute_path(self, path):
        path_a = path.replace('\"', "")
        abs_path = f'../Archivos{path_a}'
        return abs_path
