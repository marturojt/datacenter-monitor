import logging                  # Logging library

# Configuracion del log
logging.basicConfig(filename='/home/pi/temperatura.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

import time                     # Time library
import board                    # Raspberry Pi GPIO management
import busio                    # IO library
import adafruit_bme280          # BME280 Sensor library
from db import dbOperations     # Database classes
from alertas import envioAlertas    # Envio de alertas

def leerInsertar(vTiempo, vIteraciones, vTemperaturaReferencia):
    """
    leerInsertar - función que realiza el insertado de los datos del sensor DHT11 en la base de datos

    Parameters
    ----------
    vTiempo : int
        tiempo que el programa va a esperar entre cada iteración
    vIteraciones : int
        numero de iteraciones que se haran en la ejecucion del programa
    vTemperaturaReferencia : int
        temperatura máxima de operacion del centro de datos
    """

    # Conexion al sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_bme280.Adafruit_BME280_I2C(i2c, address = 0x76)

    # Arrays vacios para almacenado en memoria de las mediciones
    Temp = []
    Humi = []
    Pres = []
    Alti = []

    counter = 0
    while counter < vIteraciones:
        counter += 1
        try:
            # Obtener mediciones del sensor
            Temp.append(sensor.temperature)
            Humi.append(sensor.humidity)
            Pres.append(sensor.pressure)
            Alti.append(sensor.altitude)

        except KeyboardInterrupt:
            # exits when you press CTRL+C
            logging.error("interrupcion del programa")

        except RuntimeError as error:
            logging.error(error.args[0])

        finally:
            if counter < vIteraciones:
                """
                Validacion solo para que no haga tiempo de espera al final de la última ronda
                """
                time.sleep(vTiempo)
            else:
                # Validacion de temperatura
                validaRangoTemp(max(Temp),vTemperaturaReferencia)
                logging.info("La temperatura actual es: {temper}".format(temper=max(Temp)))
                db = dbOperations()
                query = "CALL spInsertaMediciones({temp}, {humi}, {pres}, {alti});".format(temp=max(Temp), humi=max(Humi), pres=max(Pres), alti=max(Alti))
                db.execute(query)


def validaRangoTemp(actTemp, refTemp):
    """
    validaRangoTemp - Compara la temperatura actual del centro de datos

    Parameters
    ----------
    actTemp : float
        temperatura actual del centro de datos
    refTemp : int
        temperatura de referencia
    """

    if actTemp > refTemp:
        mensaje = "Temperatura elevada, la temperatura actual es: {temp}".format(temp=round(actTemp,2))
        alertas = envioAlertas()
        alertas.envioSMS(mensaje)
        alertas.envioTelegram(mensaje)
        logging.critical(mensaje)


def main():
    """
    main - Aqui solo se hace el llamado a las funciones del script
    """
    tiempo = 5                      # Tiempo de espera entre cada lectura
    iteraciones = 5                 # Número de lecturas a realizar
    temperaturaReferencia = 30      # Temperatura máxima a la que debe de estar el centro de datos
    logging.info("Inicia ejecucion del programa. Temp de referencia: {temp}. Iteraciones: {iter}. Tiempo entre iteraciones: {tempo}".format(temp=tiempo, iter=iteraciones, tempo=tiempo))
    leerInsertar(vTiempo=tiempo, vIteraciones=iteraciones, vTemperaturaReferencia=temperaturaReferencia)

if __name__ == "__main__":
    main()
