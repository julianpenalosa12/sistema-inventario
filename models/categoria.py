import mysql.connector
from config import db_config

class Categoria:

    @staticmethod
    def obtener_todas():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM categorias")
        categorias = cursor.fetchall()

        cursor.close()
        conexion.close()

        return categorias


    @staticmethod
    def crear(nombre, descripcion):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        INSERT INTO categorias (nombre, descripcion)
        VALUES (%s, %s)
        """

        cursor.execute(sql, (nombre, descripcion))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def eliminar(id_categoria):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM categorias WHERE id_categoria=%s", (id_categoria,))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def obtener_por_id(id_categoria):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM categorias WHERE id_categoria=%s", (id_categoria,))
        categoria = cursor.fetchone()

        cursor.close()
        conexion.close()

        return categoria


    @staticmethod
    def actualizar(id_categoria, nombre, descripcion):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        UPDATE categorias
        SET nombre=%s, descripcion=%s
        WHERE id_categoria=%s
        """

        cursor.execute(sql, (nombre, descripcion, id_categoria))
        conexion.commit()

        cursor.close()
        conexion.close()