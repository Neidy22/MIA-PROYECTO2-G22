from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    resp = {
        "message": "La aplicación se ha conectado"
    }
    return resp


if __name__ == "__main__":
    app.run(debug=True)
