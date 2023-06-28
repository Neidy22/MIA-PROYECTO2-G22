from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from Usuario import Usuario
from aes import CipherA

import requests


# Variable que me va a permitir manejar todos los comandos ya sea en el server, bucket

console_log = ''
ip = ''
usuarios = []  # Lista en donde se guardan los usuarios para iniciar sesion


class App():

    def __init__(self):
        self.console_log = ''
        self.root = Tk()
        self.ip = Entry(self.root)
        self.ip.place(x=25, y=25, width=200)

        def obtener():
            global ip
            ip = self.ip.get()
            self.connect_request()

        self.btn = ttk.Button(self.root, text='Connect',
                              command=obtener)
        self.btn.pack()
        self.response_label = ttk.Label(self.root, text='')
        self.response_label.pack()
        self.root.mainloop()
        login_window()


# -------------------------------------------------------------------REQUESTS-------------------------------------------------------------------


    def connect_request(self):
        global ip
        url = f'http://{ip}:5000'  # --> endpoint para probar la conexión
        # url = 'http://127.0.0.1:5000/'

        # try:
        response = requests.get(url)  # --> para enviar el url
        # si la conexión fue exitosa
        self.response_label.config(text=response.json()['message'])
        self.root.destroy()
        login_window()

        # except:
        #    self.response_label.config(
        #        text='No se ha podido conectar! Inténtelo de nuevo')


def send_input(input_text):
    global console_log, ip
    try:
        url = f'http://{ip}:5000/command'
        # url = 'http://127.0.0.1:5000/command'
        response = requests.post(url, data=input_text)
        console_log = response.content.decode()
    except:
        console_log = "Ocurrió un error! No se puede procesar tu petición"


def send_input_file(input_file):
    global console_log, ip
    try:
        url = f'http://{ip}:5000/file_input'
        # url = 'http://127.0.0.1:5000/command'
        response = requests.post(url, data=input_file)
        console_log = response.content.decode()
    except:
        console_log = "Ocurrió un error! No se puede procesar tu petición"


# -------------------------------------------------------------------VENTANAS-------------------------------------------------------------------

def login_window():
    raiz = Tk()
    raiz['bg'] = 'black'
    raiz.geometry('450x500')
    raiz.title('Ventana Principal')
    t = ttk.Label(raiz, text="Inicio de sesión",
                  background='cyan', font='Arial')
    t.place(x=165, y=20)
    txtUsr = ttk.Label(raiz, text="Usuario")
    txtUsr.place(x=100, y=58)
    txtUsr = ttk.Label(raiz, text="Contraseña")
    txtUsr.place(x=100, y=110)
    leerUsuarios()

    def obtener():  # Método del botón
        usr = cajaUsr.get()
        contra = cajaContra.get()
        iniciarSesion(usr, contra)  # Iniciando sesion

    cajaUsr = Entry(raiz)
    # Caja de texto del nombre de usuario
    cajaUsr.place(x=100, y=80, width=200)
    cajaContra = Entry(raiz)
    # Caja de texto de la contraseña
    cajaContra.place(x=100, y=132, width=200)
    # Enviar a validarCredenciales()

    # CAMBIAR A obtener PARA INICIAR SESION
    b = ttk.Button(raiz, text="Iniciar Sesión", command=obtener)

    b.place(x=175, y=180)
    # Salir y terminar el programa
    ttk.Button(raiz, text='Salir', command=raiz.destroy).pack(side=BOTTOM)
    raiz.mainloop()


# Lee los usuarios del usuarios.txt
def leerUsuarios():
    global usuarios
    # Reemplazar por la ruta del usuarios.txt
    archivoUsuarios = open("../Archivos/usuarios.txt")
    encriptado = archivoUsuarios.readlines()
    lineas = []
    for l in encriptado:
        line = l.replace("\n", "")
        lineas.append(line)
    contador = 0  # Contador para ver si la linea es par o impar
    usrs = []
    contras = []
    for linea in lineas:
        if contador % 2 == 0:
            # La linea es de un nombre de usuario
            usrs.append(linea)
        else:
            # La linea es de una contrasena
            cifrado = CipherA('miaproyecto12345')
            desencriptada = cifrado.decrypt(linea)  # Se desencripta la linea
            contras.append(desencriptada)
        contador += 1
    # Llenando la lista de usuarios
    contadorUsuarios = 0
    for u in usrs:
        usuario = Usuario(u, contras[contadorUsuarios])
        usuarios.append(usuario)
        contadorUsuarios += 1
    archivoUsuarios.close()


# Metodo de validacion de credenciales
def iniciarSesion(usr: str, contra: str):
    global usuarios
    encontrado = False
    mensaje = ""
    for u in usuarios:
        if usr == u.usuario:
            if contra == u.contrasena:
                mensaje = "Inicio de sesion exitoso"
                # Setear texto
                mostrarInicio()
            else:
                mensaje = "Inicio de sesion fallido"
                # Setear mensaje
            encontrado = True
    if not (encontrado):
        mensaje = "Inicio de sesion fallido"
        # Setear mensaje
    return mensaje


def mostrarInicio():  # Ventana a la que se ingresa si es que se inició sesión
    v = Tk()
    v.title("Página de Inicio")
    v.geometry('850x700')
    v.resizable(False, False)

    v['bg'] = 'gray'
    t = ttk.Label(v, text="INPUT", background='gray')
    t.place(x=50, y=185)

    t2 = ttk.Label(v, text="OUTPUT", background='gray')
    t2.place(x=50, y=385)

    def obtener_console_text():
        input_log = consola_in.get("1.0", "end-1c")
        send_input(input_log)
        consola_out.insert('end', console_log)

    b = ttk.Button(v, text="Reporte", command=obtener_console_text)
    b.place(x=700, y=175)

    bCerrarS = ttk.Button(v, text="Cerrar Sesión", command=v.destroy, width=12)
    bCerrarS.place(x=375, y=650)

    # Explorador de archivos
    def cargar_archivo():

        archivo = filedialog.askopenfilename(filetypes=[("Todos los archivos", "*.*")])

        if archivo:
            print("Archivo seleccionado:", archivo)
            # Lógica de lectura del archivo

            with open(archivo, 'r') as f:
                body = f.read()
                send_input_file(body)
                consola_out.insert('end', console_log)

    boton_cargar = ttk.Button(v, text="Cargar archivo", command=cargar_archivo)
    boton_cargar.place(x=10, y=10)

    # consolas
    consola_in = Text(v, height=10, width=90)
    consola_in.place(x=50, y=205)

    consola_out = Text(v, height=10, width=90)
    consola_out.place(x=50, y=405)
    consola_out.insert('end', console_log)
    v.mainloop()


App()
# mostrarInicio()
