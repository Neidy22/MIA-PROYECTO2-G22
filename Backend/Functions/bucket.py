import os
import boto3


class Bucket:

    @classmethod
    def create(self, ruta, nombre, contenido):
        mensaje = ""
        raiz = "nombreBucket/Archivos/"
        rutaArchivo = raiz+ruta+nombre
        try:
            s3 = boto3.client('s3') #Conectandome a s3
            s3.put_object(Body=contenido, Bucket='mi-bucket', Key=rutaArchivo) #Creando el archivo
            mensaje = "Se ha creado el archivo en el bucket, en la ruta " + ruta + nombre
        except Exception as e:
            mensaje = "Error al crear el archivo"
            print(e) #Si da error, en la consola se ve el error para corregir el metodo
        return mensaje