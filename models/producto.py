import mysql.connector
from config import db_config

class Producto:

    @staticmethod
    def obtener_todos():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT p.*, c.nombre AS categoria
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        """

        cursor.execute(sql)
        productos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return productos


    @staticmethod
    def crear(nombre, descripcion, precio, stock, id_categoria):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria)
        VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def eliminar(id_producto):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM productos WHERE id_producto=%s", (id_producto,))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def obtener_por_id(id_producto):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM productos WHERE id_producto=%s", (id_producto,))
        producto = cursor.fetchone()

        cursor.close()
        conexion.close()

        return producto


    @staticmethod
    def actualizar(id_producto, nombre, descripcion, precio, stock, id_categoria):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        UPDATE productos
        SET nombre=%s, descripcion=%s, precio=%s, stock=%s, id_categoria=%s
        WHERE id_producto=%s
        """

        cursor.execute(sql, (nombre, descripcion, precio, stock, id_categoria, id_producto))
        conexion.commit()

        cursor.close()
        conexion.close()
    
    @staticmethod
    def buscar(nombre):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        sql = """
        SELECT p.*, c.nombre AS categoria
        FROM productos p
        LEFT JOIN categorias c ON p.id_categoria = c.id_categoria
        WHERE p.nombre LIKE %s
        """

        cursor.execute(sql, ('%' + nombre + '%',))
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

        return resultados    
