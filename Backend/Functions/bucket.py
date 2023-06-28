import boto3
import os
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
        ruta = self.get_absolute_path(ruta)    
        #Crear las carpetas en el bucket si no existen
        carpetas = ruta.strip('/').split('/')
        carpeta_actual = ''
        for carpeta in carpetas:
            carpeta_actual += carpeta + '/'
            if not s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=carpeta_actual).get('Contents'):
                s3.put_object(Bucket=BUCKET_NAME, Key=carpeta_actual)
        
        #Creando el archivo en la ruta completa
        rutaArchivo = ruta.strip('/') + '/' + nombre
        print("Ruta del archivo = " + rutaArchivo)
        
        try:
            s3.put_object(Bucket=BUCKET_NAME, Key=rutaArchivo, Body=contenido)
            mensaje = f"Archivo creado en el bucket, en la ruta: {rutaArchivo}"
        except Exception as e:
            mensaje = f"Error al crear el archivo debido a la excepción: {str(e)}"
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
    def copyBucketBucket(self, origen, destino): #REVISADA
        origen = self.get_absolute_path(origen)
        destino = self.get_absolute_path(destino)
        
        # Verificando existencia de las rutas
        existeOrigen = False
        objetos = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=origen)
        if 'Contents' in objetos:
            existeOrigen = True
        if not existeOrigen:
            return "La ruta de origen no existe en el bucket."

        existeDestino = False
        objetos = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=destino)
        if 'Contents' in objetos:
            existeDestino = True
        if not existeDestino:
            return "La ruta de destino no existe en el bucket."
        #Fin verificacion
        
        if origen.endswith('/'): #Si el origen es una carpeta
            #Lista de objetos
            objetos = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=origen) #Sustituir el nombre del bucket

            if 'Contents' not in objetos:
                return "No se encontraron archivos en la carpeta de origen."

            # Copiar cada archivo a la carpeta de destino
            for objeto in objetos['Contents']:
                origen_archivo = objeto['Key']
                destino_archivo = destino + origen_archivo.split('/')[-1]  #Construyendo la ruta de destino
                s3.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': origen_archivo}, Key=destino_archivo)
            return "Los archivos han sido copiados exitosamente."
        else: #Si el origen es un archivo
            try:
                s3.head_object(Bucket=BUCKET_NAME, Key=origen)
                s3.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': origen}, Key=destino) #Copiando el archivo
                return "Archivo copiado exitosamente."
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    return "El archivo a copiar no existe."
                else:
                    return "Se produjo un error al verificar el archivo de origen."
                
    @classmethod
    def copiarBucketServer(self, origen, destino): #REVISADA
        #Enlazando las dos rutas a la carpeta raiz: Archivos
        origen = self.get_absolute_path(origen) 
        destino = self.get_absolute_path(destino)
        
        #Verificando que exista la ruta en el bucket
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=origen)
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return "La ruta de origen no existe en el bucket."
            else:
                return "Se produjo un error al verificar la ruta de origen."

        #Verificando si la ruta de destino en el server existe
        if not os.path.exists(destino):
            return "La ruta de destino en la máquina virtual no existe."

        if origen.endswith('/'): #La ruta de origen es de una carpeta
            objetos = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=origen)

            if 'Contents' not in objetos:
                return "No se encontraron archivos en la carpeta de origen."

            #Copiando cada archivo de la carpeta de origen
            for objeto in objetos['Contents']:
                origenArchivo = objeto['Key']
                nombreArchivo = origenArchivo.split('/')[-1]
                destinoArchivo = os.path.join(destino, nombreArchivo) #Ruta de destino construida
                s3.download_file(Bucket=BUCKET_NAME, Key=origenArchivo, Filename=destinoArchivo)
            return "Los archivos han sido copiados exitosamente a la máquina virtual."
        else:
            #La ruta de origen es de un archivo
            if not os.path.isdir(destino):
                return "La ruta de destino no existe en la máquina virtual"

            #Obteniendo el nombre del archivo de origen
            nombreArchivo = os.path.basename(origen)

            #Construyendo la ruta de destino en el server
            destinoArchivo = os.path.join(destino, nombreArchivo)

            #Copiando el archivo
            s3.download_file(Bucket=BUCKET_NAME, Key=origen, Filename=destinoArchivo)
            return "El archivo ha sido copiado exitosamente a la máquina virtual."

        
    @classmethod
    def copyServerBucket(self, origen, destino): #REVISADO
        s3 = boto3.client('s3')
        origen = self.get_absolute_path(origen)
        destino = self.get_absolute_path(destino)
        #Verificando si la ruta de origen existe
        if not os.path.exists(origen):
            return "La ruta de origen en el server no existe. :("

        #Verificando si la ruta destino existe
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=destino)
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return "La ruta de destino en el bucket no existe. :("
            else:
                return "Se produjo un error al verificar la ruta de destino en el bucket."

        if os.path.isdir(origen): 
            #La ruta a copiar es de una carpeta
            archivos = os.listdir(origen)
            if not archivos:
                return "No se encontraron archivos en la carpeta de origen."

            #Copiando cada archivo en la carpeta hacia la carpeta destino
            for archivo in archivos:
                rutaArchivo = os.path.join(origen, archivo)
                destinoArchivo = os.path.join(destino, archivo)
                s3.upload_file(Filename=rutaArchivo, Bucket=BUCKET_NAME, Key=destinoArchivo)
            return "Los archivos han sido copiados exitosamente al bucket."
        else:
            #El origen es un archivo
            archivo = os.path.basename(origen)
            destinoArchivo = os.path.join(destino, archivo)
            s3.upload_file(Filename=origen, Bucket=BUCKET_NAME, Key=destinoArchivo)
            return "El archivo ha sido copiado exitosamente al bucket."


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
        #Verificar si la ruta de origen existe
        try:
            s3.head_object(Bucket=BUCKET_NAME, Key=ruta)
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                return "La ruta del archivo o carpeta no existe."
            else:
                return "Se produjo un error al verificar la ruta de origen."

        #Extraer el nombre del archivo o carpeta actual
        nombreActual = ruta.split('/')[-1]
        #Extraer la ruta de la carpeta padre
        rutaPadre = ruta.rsplit('/', 1)[0]
        #Construir la ruta de destino con el nuevo nombre
        rutaDestino = rutaPadre + '/' + nuevoNombre

        try:
            #Verificando si la ruta de destino ya existe
            s3.head_object(Bucket=BUCKET_NAME, Key=rutaDestino)
            return "Ya existe un archivo o carpeta con el nuevo nombre."
        except s3.exceptions.ClientError as e:
            if e.response['Error']['Code'] != '404':
                return "Se produjo un error al verificar la ruta de destino."

        #Renombrando el archivo o carpeta
        try:
            s3.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': ruta}, Key=rutaDestino)  #Renombrar
            s3.delete_object(Bucket=BUCKET_NAME, Key=ruta)
            return "Se renombró exitosamente."
        except s3.exceptions.ClientError as e:
            return "Se produjo un error al renombrar el archivo o carpeta."

    @classmethod
    def recovery(self):
        pass

    def backupServerToBucket(self, nombre_backup):
        ruta_archivos = '/home/ubuntu/Archivos/'
        ruta_backup = '/home/ubuntu/' + nombre_backup + '/'
        try:
            s3.put_object(Bucket=BUCKET_NAME, Key=nombre_backup + '/')

            #Se obtiene la lista de los archivos o carpetas
            contenido = os.listdir(ruta_archivos)
            
            #Se sube cada archivo dentro de la carpeta del bucket
            for item in contenido:
                ruta_item = os.path.join(ruta_archivos, item)

                if os.path.isfile(ruta_item):
                    #Se sube el archivo al bucket
                    ruta_destino = nombre_backup + '/' + item
                    s3.upload_file(ruta_item, BUCKET_NAME, ruta_destino)
                elif os.path.isdir(ruta_item):
                    #Se sube todo el contenido de la carpeta en forma recursiva
                    subcarpeta = item + '/'
                    ruta_destino = nombre_backup + '/' + subcarpeta
                    subcontenido = os.listdir(ruta_item)

                    for subitem in subcontenido:
                        ruta_subitem = os.path.join(ruta_item, subitem)
                        ruta_subdestino = ruta_destino + subitem
                        s3.upload_file(ruta_subitem, BUCKET_NAME, ruta_subdestino)

            return "Se ha hecho un backup del server en el bucket: " + BUCKET_NAME
        except Exception as e:
            print("Error Backup ServerToBucket> " + str(e))
            return "Error al realizar el backup: "

    @classmethod
    def backupBucketToBucket(self, nombre_backup):
        ruta_archivos = '/home/ubuntu/Archivos/'
        ruta_backup = '/home/ubuntu/' + nombre_backup + '/'

        try:
            #Se obtiene la lista de archivos o carpetas
            contenido = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=ruta_archivos)

            for objeto in contenido['Contents']:
                ruta_objeto = objeto['Key']
                nombre_objeto = ruta_objeto.replace(ruta_archivos, '')

                if nombre_objeto:
                    #Se sube el objeto a la carpeta del backup
                    ruta_destino = nombre_backup + '/' + nombre_objeto
                    s3.copy_object(Bucket=BUCKET_NAME, CopySource={'Bucket': BUCKET_NAME, 'Key': ruta_objeto}, Key=ruta_destino)

            return "El backup se ha creado exitosamente en el bucket: " + BUCKET_NAME
        except Exception as e:
            print("Error backup BucketToBucket: " + str(e))
            return "Error al realizar el backup: "
        
    @classmethod
    def backupBucketToServer(self, nombre_backup):
        ruta_archivos = '/home/ubuntu/Archivos/'
        ruta_backup = '/home/ubuntu/' + nombre_backup + '/'
        try:
            #Creando la carpeta del backup en el server
            os.makedirs(ruta_backup)
            #Obteniendo la lista de archivos y carpetas
            contenido = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=ruta_archivos)

            for objeto in contenido['Contents']:
                ruta_objeto = objeto['Key']
                nombre_objeto = ruta_objeto.replace(ruta_archivos, '')

                if nombre_objeto:
                    #Descargando el objeto y guardandolo en la carpeta del backup
                    ruta_destino = os.path.join(ruta_backup, nombre_objeto)
                    s3.download_file(BUCKET_NAME, ruta_objeto, ruta_destino)
                    
            return "El backup se ha creado exitosamente en la máquina virtual en la ruta: " + ruta_backup
        except Exception as e:
            print("errorBackup BucketServer " + str(e))
            return "Error al realizar el backup."

    @classmethod
    def delete_all(self):  
        ruta = '/home/ubuntu/Archivos/' #Reemplazar con la ruta que estara en el bucket
        objetos = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=ruta) #Obteniendo todos los objetos en el bucket
        
        if 'Contents' in objetos: #Si hay objetos en la carpeta
            for objeto in objetos['Contents']:
                s3.delete_object(Bucket=BUCKET_NAME, Key=objeto['Key']) #Borrando cada objeto de la carpeta
                
        return "Se ha vaciado la carpeta archivos."

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
