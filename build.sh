# Shell
set -o errexit # si encuentra un error termina el proceso

# Instalamos las dependencias
pipenv install

# Va a ejecutar las migraciones de la base de datos
pipenv run upgrade