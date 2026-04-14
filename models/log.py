import mysql.connector
from config import db_config

class Log:

    @staticmethod
    def registrar(id_usuario, accion):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        INSERT INTO logs (accion, id_usuario)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (accion, id_usuario))
        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def obtener_todos():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
        SELECT logs.*, usuarios.nombre AS usuario
        FROM logs
        INNER JOIN usuarios 
        ON logs.id_usuario = usuarios.id_usuario
        ORDER BY logs.fecha DESC
        """)

        logs = cursor.fetchall()

        cursor.close()
        conexion.close()

        return logs