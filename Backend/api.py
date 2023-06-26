# coding=utf-8
from flask import Flask, request
from myFileSystem import myFileSystem
app = Flask(__name__)


@app.route("/")
def welcome():
    resp = {
        "message": "La aplicación se ha conectado"
    }
    return resp


@app.route("/command", methods=['POST'])
def input_command():
    data_input = request.data.decode()

    msg = 'Debes ingresar un comando válido!'
    if data_input != '':

        msg = myFileSystem.run_console_input(data_input)

    return msg


if __name__ == "__main__":
    app.run(debug=True)
