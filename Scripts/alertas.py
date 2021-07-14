import logging                  # Logging library

# Configuracion del log
logging.basicConfig(filename='/home/pi/temperatura.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

from data import keyQuiubas, keyTelegram    # Clases con datos de conexion de telegram y quiubas
from telegram.bot import Bot                # Telegram library
import requests                             # HTTP Methods

class envioAlertas():
    """
    envioAlertas - Clase para el envio de alertas por SMS o Telegram
    """

    def __init__(self):
        """
        __init__ - Datos para consumir el servicio de SMS
        """
        self.API_KEY = keyQuiubas.API_KEY
        self.API_SECRET = keyQuiubas.API_SECRET
        self.url = keyQuiubas.url
        self.numeros = keyQuiubas.numeros_alerta
        self.BOT_KEY = keyTelegram.BOT_KEY
        self.chatID = keyTelegram.chatID

    def envioSMS(self, vMensaje):
        """
        envioSMS - Envio de un SMS a la lista de números configurada

        Parameters
        ----------
        vMensaje : string
            Mensaje que será enviado por SMS
        """
        for telefono in self.numeros:
            smsData = {'to_number':telefono,'message':vMensaje}
            resSMS = requests.post(self.url, data = smsData, auth = (self.API_KEY, self.API_SECRET))
            if resSMS.status_code != 200:
                logging.error("Error en envio de SMS = {}".format(resSMS.text))
            else:
                logging.info(resSMS.text)

    def envioTelegram(self, vMensaje):
        """
        envioTelegram - Envio de un mensaje de telegram

        Parameters
        ----------
        vMensaje : string
            Mensaje que será enviado por SMS
        """
        bot = Bot(self.BOT_KEY)
        bot.send_message(chat_id=self.chatID,text=vMensaje)
