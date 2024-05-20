**Clonar este repositorio**

   git clone https://github.com/coderunner86/proyecto_1.git

**Crear un entorno virtual**

    python3 -m venv venv

**Activar el entorno**

    source venv/bin/activate

**Instalar el requirements**

    pip install -r requirements.txt

**Generar un Token de Acceso**
*METODO POST*
Realizar una solicitud para crear el TOKEN

    curl -X POST -d "grant_type=password&username=admin&password=admin&client_id=fVDN0p5YufIhzroLf0RKlNpp8HVsDVUiLoQCJbkw&client_secret=d8C0STSoLdXhK6A90ru3Bb7clVjIQnoiWzmFmQS9FRbiMoSkz2oosMYT3qSHaYGaurZ4NA0TQdzCx2zEg6mlTm4lVOav3rzEKZonDFXWuQlQqSma3JmlYqC2TrkxexPY" http://127.0.0.1:8000/o/token/

_RESPUESTA_

   {"access_token": "9e8vyabDHDD4JLdLR4S16R77gkxsiI", "expires_in": 36000, "token_type": "Bearer", "scope": "read write", "refresh_token": "WDx1DRWPl5M9ChG6pZdawLbnWbBPm2"}

**Usar el Token**
*METODO POST*
Realizar una solicitud de creacion de usuario:

    curl -X POST -H "Authorization: Bearer 9e8vyabDHDD4JLdLR4S16R77gkxsiI" -H "Content-Type: application/json" -d '{"nombre": "Juan", "apellido": "Pérez", "tipo": "comprador", "direccion": "Calle Falsa 123", "ciudad": "Ciudad Ejemplo"}' http://127.0.0.1:8000/crear/

_RESPUESTA_

   {"id":1,"nombre":"Juan","apellido":"Pérez","direccion":"Calle Falsa 123","tipo":"comprador","ciudad":"Ciudad Ejemplo","longitud":0.0,"latitud":0.0,"estado_geo":false,"cargo":null}

**Listar Usuarios**
*METODO GET*
Realizar la solicitud incluyendo el token de acceso en el encabezado de autorización:

    curl -X GET -H "Authorization: Bearer 9e8vyabDHDD4JLdLR4S16R77gkxsiI" http://127.0.0.1:8000/lista/

_RESPUESTA_

   [{"id":1,"nombre":"Juan","apellido":"Pérez","direccion":"Calle Falsa 123","tipo":"comprador","ciudad":"Ciudad Ejemplo","longitud":0.0,"latitud":0.0,"estado_geo":false,"cargo":null}]

**Obtener un usuario por id**
*METODO GET*
Realizar la solicitud incluyendo el token en el encabezado:

    curl -X GET -H "Authorization: Bearer 9e8vyabDHDD4JLdLR4S16R77gkxsiI" http://127.0.0.1:8000/usuario/1/

_RESPUESTA_

   {"id":1,"nombre":"Juan","apellido":"Pérez","direccion":"Calle Falsa 123","tipo":"comprador","ciudad":"Ciudad Ejemplo","longitud":0.0,"latitud":0.0,"estado_geo":false,"cargo":null}(venv) 

**Eliminar un usuario por id**
*METODO DELETE*

    curl -X DELETE -H "Authorization: Bearer 8KJjab3Bi62V9axfffUQlS9BlQ1qIr" http://127.0.0.1:8000/eliminar/1/

**Geocodificar base**
*METODO GET*
Realizar la solicitud incluyendo el token en el encabezado:
    curl -X GET -H "Authorization: Bearer 9e8vyabDHDD4JLdLR4S16R77gkxsiI" http://127.0.0.1:8000/geocodificar_base/   

_RESPUESTA_

   {"status":"Geocodificación completada."}
