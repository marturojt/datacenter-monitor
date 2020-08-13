from data import connMysql # Datos de conexion para mysql
import pymysql             # Libreria para conectarnos a la base de datos

class dbOperations():
    """
    dbOperations - Clase para las operaciones que se van a realizar en la base de datos de mysql
    """

    def __init__(self):
        """
        __init__ - Datos de la conexión a la base de datos
        """
        self.host = connMysql.address
        self.user = connMysql.user
        self.password = connMysql.passw
        self.db = connMysql.db

    def __connect__(self):
        """
        __connect__ - Conexión a la base de datos
        """
        self.con = pymysql.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            db = self.db,
            cursorclass = pymysql.cursors.DictCursor
        )
        self.cur = self.con.cursor()

    def __disconnect__(self):
        """
        __disconnect__ - Desconexión de la base de datos
        """
        self.con.close()

    def fetch(self, sql):
        """
        fetch - Ontener informaciónd de la base de datos mediante un comando tal como SELECT

        Parameters
        ----------
        sql : string
            Query o instrucción a ejecutar en la base de datos del cual se espera recibir un resultado
        """
        self.__connect__()
        self.cur.execute(sql)
        result = self.cur.fetchall()
        self.__disconnect__()
        return result

    def execute(self, sql):
        """
        execute - Ejecutar un comando en la base de datos del cual no es necesario obtener una respuesta

        Parameters
        ----------
        sql : string
            Query o instrucción para ejecutar en la base de datos
        """
        self.__connect__()
        self.cur.execute(sql)
        self.con.commit()
        self.__disconnect__()
