# Flask Template


1. `pipenv shell` -> para crear mi entorno virtual
2. `pipenv install flask` -> Para instalar la dependencia de flask
3. creamos la carpeta src con el archivo app.py

```py
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
```
4. `flask --app src.app run` -> Flask, --app src.app Señala donde esta nuestra aplicacion. run se encarga de ejecutarla
5. Agregar al pipfile el comando `start|dev` para no tener que escribir el comando anterior cada vez que queramos ejecutar el proyecto


## Migrations

`pipenv install flask_migrate`

`flask --app src.app db init`