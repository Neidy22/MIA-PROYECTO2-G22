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
    def create(self, ruta, nombre, contenido):
        mensaje = ""
        ruta = self.get_absolute_path(ruta)
        rutaArchivo = ruta+nombre
        try:
            carpetas = ruta.split('/')  #Separando las carpetas de la ruta
            carpetaActual = ''
            #Si las carpetas que conforman la ruta no existen, se crean
            for carpeta in carpetas:
                if carpetaActual:
                    existeCarpeta = s3.list_objects_v2(Bucket='nombreBucket', Prefix=carpetaActual)
                    if 'Contents' not in existeCarpeta:
                        #La lista de objetos con el prefijo de la carpetaActual está vacía, no existe la carpeta, se crea
                        s3.put_object(Bucket='nombreBucket', Key=carpetaActual)
                
                carpetaActual = os.path.join(carpetaActual, carpeta)
            
            #Crear el archivo en la ruta completa
            s3.put_object(Bucket='nombreBucket', Key=rutaArchivo, Body=contenido)
            mensaje = "Archivo creado en Amazon S3, en la ruta: " + ruta
        except Exception as e:
            mensaje = "Error al crear el archivo por la excepcion: " + str(e)
        return mensaje

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
    def copyBucketBucket(self, origen, destino):
        bucket = "NombreBucket" #Reemplazar con el nombre de mi bucket
        origen = self.get_absolute_path(origen)
        destino = self.get_absolute_path(destino)
        if origen.endswith('/'): #Si el origen es una carpeta
            #Lista de objetos
            objetos = s3.list_objects_v2(Bucket=bucket, Prefix=origen) #Sustituir el nombre del bucket

            if 'Contents' not in objetos:
                return "No se encontraron archivos en la carpeta de origen."

            # Copiar cada archivo a la carpeta de destino
            for objeto in objetos['Contents']:
                origen_archivo = objeto['Key']
                destino_archivo = destino + origen_archivo.split('/')[-1]  #Construyendo la ruta de destino
                s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': origen_archivo}, Key=destino_archivo)
            return "Los archivos han sido copiados exitosamente."
        else: #Si el origen es un archivo
            try:
                s3.head_object(Bucket=bucket, Key=origen)
                s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': origen}, Key=destino) #Copiando el archivo
                return "Archivo copiado exitosamente."
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    return "El archivo a copiar no existe."
                else:
                    return "Se produjo un error al verificar el archivo de origen."

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
    def rename(self, ruta, nuevoNombre):
        ruta = self.get_absolute_path(ruta)
        bucket = "NombreBucket"
        # Verificar si la ruta de origen existe
        try:
            s3.head_object(Bucket=bucket, Key=ruta)
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return "La ruta del archivo o carpeta no existe."
            else:
                return "Se produjo un error al verificar la ruta de origen."

        #Ruta destino ya con el nuevo nombre
        ruta_destino = ruta.rsplit('/', 1)[0] + '/' + nuevoNombre

        try:
            s3.head_object(Bucket=bucket, Key=ruta_destino)
            s3.copy_object(Bucket=bucket, CopySource={'Bucket': bucket, 'Key': ruta}, Key=ruta_destino) #Renombrando
            s3.delete_object(Bucket=bucket, Key=ruta)
            return "Se ha aplicado el rename exitosamente."
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] != '404':
                return "No es posible renombrar, ya existe el nombre."

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
