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


@app.route("/file_content", methods=['GET'])
def send_file_content():
    command = request.params
    msg = myFileSystem.send_file_content(
        command.get('type'), command.get('name'))

    return msg


if __name__ == "__main__":
    host = '0.0.0.0'
    port = '5000'
    app.run(host=host, port=port)
