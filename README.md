# datacenter-monitor
Monitoreo de temperatura y humedad del datacenter usando una raspberry pi y un sensor BME280 Bosh



## Configuración

Credenciales de los servicios de terceros (Quiubas, telegram y MySQL):
- Copiar el archivo Scripts/data.py.dist a Scripts/data.py
- Dentro del archivo Scripts/data.py ingresar las credenciales correspondientes

Instalación de la base de datos:
- Crear una nueva base de datos en MySQL
- Cargar el archivo Database/database.sql el cual contiene la estructura de la tabla y el procedimiento almacenado necesario para el funcionamiento del proyecto

        mysql -u USUARIO -p NOMBREDELABASE < Database/database.sql

NOTA: De forma inicial es necesario cargar en la tabla tbMetodosBot los siguientes valores, estos valores estan relacionados con el procedimiento almacenado llamado 'spMetodosBOT'

| idtbMetodosBot | nombreMetodo |
| --- | --- |
| 1 | Temp. Actual |
| 2 | Temp. Promedio |
| 3 | Temp. Máxima |
