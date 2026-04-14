import mysql.connector
from config import db_config

class Movimiento:

    @staticmethod
    def crear(id_producto, tipo, cantidad, id_usuario):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        # validación stock
        if tipo == "salida":
            cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
            stock_actual = cursor.fetchone()[0]

            if cantidad > stock_actual:
                conexion.close()
                return False

        # insertar movimiento
        cursor.execute("""
        INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, id_usuario)
        VALUES (%s, %s, %s, %s)
        """, (id_producto, tipo, cantidad, id_usuario))

        # actualizar stock
        if tipo == "entrada":
            cursor.execute("UPDATE productos SET stock = stock + %s WHERE id_producto = %s",
                           (cantidad, id_producto))
        else:
            cursor.execute("UPDATE productos SET stock = stock - %s WHERE id_producto = %s",
                           (cantidad, id_producto))

        conexion.commit()
        cursor.close()
        conexion.close()

    # 👇 AGREGA ESTO
    @staticmethod
    def obtener_todos():

        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
        SELECT m.id_movimiento, m.tipo_movimiento, m.cantidad, m.fecha,
               p.nombre AS producto,
               u.nombre AS usuario
        FROM movimientos m
        INNER JOIN productos p ON m.id_producto = p.id_producto
        INNER JOIN usuarios u ON m.id_usuario = u.id_usuario
        ORDER BY m.fecha DESC
        """)

        movimientos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return movimientos