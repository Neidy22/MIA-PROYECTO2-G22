from tkinter import *
from tkinter import ttk
import requests


# Variable que me va a permitir manejar todos los comandos ya sea en el server, bucket

console_log = ''


class App():

    def __init__(self):
        self.console_log = ''
        self.root = Tk()
        self.btn = ttk.Button(self.root, text='Connect',
                              command=self.connect_request)
        self.btn.pack()
        self.response_label = ttk.Label(self.root, text='')
        self.response_label.pack()
        self.root.mainloop()

    # -------------------------------------------------------------------REQUESTS-------------------------------------------------------------------

    def connect_request(self):
        global is_connected
        url = 'http://localhost:5000/'  # --> endpoint para probar la conexión

        try:
            response = requests.get(url)  # --> para enviar el url
            # si la conexión fue exitosa
            self.response_label.config(text=response.json()['message'])
            self.root.destroy()
            login_window()

        except:
            self.response_label.config(
                text='No se ha podido conectar! Inténtelo de nuevo')

        # mostrar el mensaje de respuesta para saber si la api se conectó


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

    def obtener():  # Método del botón
        usr = cajaUsr.get()
        contra = cajaContra.get()
        # iniciarSesion(usr, contra)  # enviar los datos de inicio
        raiz.destroy()
        mostrarInicio()

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


def mostrarInicio():  # Ventana a la que se ingresa si es que se inició sesión

    v = Tk()
    v.title("Página de Inicio")
    v.geometry('1050x500')
    v['bg'] = 'gray'
    t = ttk.Label(v, text="Consola", background='gray')
    t.place(x=50, y=45)

    def obtener():
        result = b.get()
    b = ttk.Button(v, text="Botón Prueba", command=obtener)
    b.place(x=55, y=100)

    bCerrarS = ttk.Button(v, text="Cerrar Sesión", command=v.destroy, width=11)
    bCerrarS.place(x=500, y=450)

    # consolas
    Consola = Text(v, height=20, width=90)
    Consola.place(x=50, y=75)
    Consola.insert('end', console_log)
    v.mainloop()


App()
