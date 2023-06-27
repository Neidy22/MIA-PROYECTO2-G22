import boto3
from creds import REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

# indicando que voy  a consumir el servicio de s3 con las credenciales
# s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
#                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name=REGION)
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
        path = self.get_absolute_path(path)

        try:
            if name != None:  # eliminar archivo
                name = name.strip('\"')
                s3_resource.Object(BUCKET_NAME, path + name).delete()
                msg = "Se ha eliminado el archivo en la ruta {} correctamente".format(
                    path+name)
            else:  # eliminar carpeta
                s3_resource.Object(BUCKET_NAME, path).delete()
                msg = "Se ha eliminado la carpeta en la ruta {} correctamente".format(
                    path)

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
    def transfer(self):
        pass

    @classmethod
    def recovery(self):
        pass

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
    def get_absolute_path(self, path):
        path_a = path.replace('\"', "")
        # path_a = path_a.replace('/', '\\')
        abs_path = f'Archivos{path_a}'
        return abs_path


# print(Bucket.delete('/"pruebas delete"/', None))
# print(Bucket.modify('/"Pruebas a modificar"/modificar.txt',
#      "Este es el contenido nuevo probando s3"))
print(Bucket.open(None, None, '/"Pruebas a modificar"/modificar.txt'))
