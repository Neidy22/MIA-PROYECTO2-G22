import os
import boto3
from creds import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from pathlib import Path

# indicando que voy  a consumir el servicio de s3 con las credenciales
s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

s3_resource = boto3.resource('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)

# buckets = s3.list_buckets()

# for bucket in buckets['Buckets']:
#    print('Bucket Name: {}'.format(bucket["Name"]))
# MY_BUCKET = buckets[0]

BUCKET_NAME = 'bucket-mia-proyecto2'


class Bucket:

    @classmethod
    def delete(self, path, name):
        msg = ''
        path = self.get_absolute_path_bucket(path)

        try:
            if name != None:  # eliminar archivo
                name = name.strip('\"')

                s3_resource.Object(BUCKET_NAME, path + name).delete()
                msg = "Se ha eliminado el archivo en la ruta {} correctamente".format(
                    path+name)
            else:  # eliminar carpeta

                # listar los elementos de la carpeta
                my_bucket = s3_resource.Bucket(BUCKET_NAME)
                elements = my_bucket.objects.filter(Prefix=path)

                # recorrer la lista y eliminar elemento por elemento
                for element in elements:
                    s3_resource.Object(BUCKET_NAME, element.key).delete()

        except:
            msg = "Ha ocurrido un error! No se puedo eliminar la ruta {} especificada".format(
                path)

        return msg

    @classmethod
    def modify(self, path, body):
        path = self.get_absolute_path(path)
        body = body.strip('\"')
        msg = ''
        try:
            # obtener el el objeto del archivo
            my_file = s3_resource.Object(BUCKET_NAME, path)
            # modificar el contenido del archivo
            my_file.put(Body=body.encode(), ContentType='text/plain')

            msg = 'Se modificó correctamente el contenido del archivo {}'.format(
                path)
        except:
            msg = 'Error! no se pudo modificar el contenido del archivo!'
        return msg

    @classmethod
    def transfer_server_bucket(self):
        pass

    @classmethod
    def transfer_bucket_server(self, from_path, to_path):
        msg = ''
        from_path = from_path.replace('"', "")
        # from_path = self.get_absolute_path_bucket(from_path)
        to_path = self.get_absolute_path_server(to_path)
        try:
            # descargar en la carpeta Archivos la ruta en el bucket
            self.download_folder(BUCKET_NAME, from_path, to_path)

            # eliminar en el bucket la ruta
            if from_path.endswith('/'):  # es una carpeta
                # print("eliminar carpeta {}".format(from_path))
                self.delete(from_path, None)

            else:  # es un archivo
                name = "/"+from_path.split('/')[-1]
                from_path = from_path.split('/')[:-1]
                from_path = "/".join(from_path)
                self.delete(from_path, name)

            msg = "Tranferencia bucket-server exitosa"

        except:
            msg = "Ocurrió un error! No se puedo realizar la transferencia bucket-server"

        return msg

    @classmethod
    def transfer_bucket_bucket(self):
        pass

    @classmethod
    def recovery_server_bucket(self, ip, port, name):
        msg = ''
        # la ruta abosulta en el proyecto en el server
        name = self.get_absolute_path_server(name)
        if ip == None and port == None:  # se trabajará sobre nuestro server y nuestro bucket
            if os.path.exists(name):
                # si la carpeta del punto de restauración existe copio el contendio de la carpeta name del server en la carpeta Archivos del bucket
                print("metodo copiar de mi server al bucket")

        else:  # se trabajará en el server del otro equipo
            pass

        return msg

    @classmethod
    def recovery_bucket_server(self, ip, port, name):
        msg = ''
        # la ruta abosulta en el proyecto en el bucket
        name = self.get_absolute_path_bucket(name)

        if ip == None and port == None:  # se trabajará sobre nuestro server y nuestro bucket

            # si la carpeta del punto de restauración existe descargo el contenido de la carpeta name en el bucker hacia la carpeta Archivos del server
            try:

                self.download_folder(BUCKET_NAME, name, '../../Archivos/')
                msg = "Recovery bucket-server exitoso"

            except:
                msg = "Ocurrió un error! No se pudo hacer el recovery bucket-server"

        else:  # se trabajará en el server del otro equipo
            pass

        return msg

    @classmethod
    def recovery_bucket_bucket(self, ip, port, name):
        msg = ''

        # la ruta abosulta en el proyecto en el bucket
        name = self.get_absolute_path_bucket(name)

        if ip == None and port == None:  # se trabajará sobre nuestro bucket
            try:
                # obtengo los elementos de la carpeta en donde está el punto de restauración
                my_bucket = s3_resource.Bucket(BUCKET_NAME)
                elements = my_bucket.objects.filter(Prefix=name)
                for element in elements:
                    # print(element.key)
                    aux_key = element.key.split('/')[2:]
                    aux_key = "/".join(aux_key)

                    dest_path = 'Archivos/' + aux_key
                    s3_resource.Object(BUCKET_NAME, dest_path).copy_from(
                        CopySource="{}/{}".format(BUCKET_NAME, element.key))

                    msg = "Recovery bucket-bucket exitoso"

            except:
                msg = "Ocurrió un error! No se pudo hacer el recovery bucket-bucket"

        else:  # se trabajará en el server del otro equipo
            pass

        return msg

    @classmethod
    def open(self, ip, port, name):
        name = self.get_absolute_path(name)

        msg = ''
        try:
            if ip == None and port == None:  # se trabajará en el propio bucket
                my_bucket = s3_resource.Object(BUCKET_NAME, name)
                my_file_content = my_bucket.get(
                )['Body'].read().decode('utf-8')
                msg = my_file_content
                msg += "\n"
            else:  # se trabajará en el bucket del otro equipo
                pass
        except:
            msg = 'Ha ocurrido un error! El archivo {} no se ha podido abrir'.format(
                name)
        return msg

    @classmethod
    def get_absolute_path_bucket(self, path):
        path_a = path.replace('\"', "")
        # path_a = path_a.replace('/', '\\')
        abs_path = f'Archivos{path_a}'
        return abs_path

    @classmethod
    def get_absolute_path_server(self, path):
        path_a = path.replace('\"', "")
        # path_a = path_a.replace('/', '\\')
        abs_path = f'../../Archivos{path_a}'
        return abs_path

    @classmethod
    def download_folder(self, bucket_name, prefix, local_directory):
        # paginator = s3.get_paginator('list_objects')

        my_bucket = s3_resource.Bucket(bucket_name)
        elements = my_bucket.objects.filter(Prefix=prefix)
        # print(elements)

        for element in elements:
            # print(element.key)

            # elimino el prefix para no volver a crear las carpetas
            aux_key = element.key.split('/')[2:]
            aux_key = "/".join(aux_key)

            actual_path = local_directory + aux_key

            if element.key.endswith('/'):  # es una carpeta
                if not os.path.exists(actual_path):
                    os.makedirs(actual_path)
            else:  # es un archivo
                # de la ruta actual le elimino la convierto en un array y le quito el último elemento que representa el nombre del archivo
                actual_file_path = actual_path.split('/')[:-1]
                # vuelvo a crear la ruta  ahora sin el nombre de archivo solo las carpetas
                actual_file_path = "/".join(actual_file_path)

                if not os.path.exists(actual_file_path):
                    os.makedirs(actual_file_path)

                s3.download_file(bucket_name, element.key, os.path.join(
                    actual_file_path, element.key.split('/')[-1]))


# print(Bucket.delete('/"pruebas delete"/', None))
# print(Bucket.modify('/"Pruebas a modificar"/modificar.txt',
#      "Este es el contenido nuevo probando s3"))
# print(Bucket.open(None, None, '/"Pruebas a modificar"/modificar.txt'))
# print(Bucket.recovery_bucket_server(None, None, '/"copia g22"/'))
# print(Bucket.recovery_bucket_bucket(None, None, '/"copia g22"/'))
print(Bucket.transfer_bucket_server('/"copia g22"/', '/"Probando"/'))
print(Bucket.transfer_bucket_server('/borrar1.txt', '/"prueba 2"/'))
