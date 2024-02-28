# P3
## Ingesta desde GitHub en Mongo DB

### Enunciado:
* Se pretende realizar una ingesta avanzada de commits.
* Desarrollar un cliente Python (u en otro lenguaje) para realizar la ingesta de commits:
    1. Se realizará la ingesta del proyecto [sourcegraph](https://github.com/sourcegraph/sourcegraph/).
    2. Se limitará a los commits producidos desde el 1 de enero 2019 hasta la actualidad.
    3. Se debe gestionar de forma eficaz y eficiente el rate limit de GitHub.
    4. Además de la información básica de cada commit, añadir dos campos nuevos a cada documento en Mongo con la información extendida de ficheros modificados y las estadísticas de cambios de cada commit.
* Utilizar Operación [‘Get a commit’](https://docs.github.com/en/rest/commits/commits#get-a-commit).

### Entrega:
* Una memoria con todas las explicaciones paso a paso y las evidencias de los resultados obtenidos.
* Se debe añadir el código Python con el código del cliente y demás ficheros de configuración.
