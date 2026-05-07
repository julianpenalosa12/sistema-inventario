import mysql.connector
from config import db_config

class Movimiento:

    @staticmethod
    def crear(id_producto, tipo, cantidad, precio, id_usuario):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        # Validar precio
        if precio is None or precio == "":
           precio = 0

        # Validar stock si es salida
        if tipo == "salida":
           cursor.execute("SELECT stock FROM productos WHERE id_producto = %s", (id_producto,))
           stock_actual = cursor.fetchone()[0]

           if cantidad > stock_actual:
              conexion.close()
              return False

        # INSERTAR movimiento (precio REAL del momento)
        cursor.execute("""
          INSERT INTO movimientos (id_producto, tipo_movimiento, cantidad, precio_unitario, id_usuario)
          VALUES (%s, %s, %s, %s, %s)
        """, (id_producto, tipo, cantidad, precio, id_usuario))

        # Actualizar stock
        if tipo == "entrada":
           cursor.execute("""
               UPDATE productos 
               SET stock = stock + %s 
               WHERE id_producto = %s
            """, (cantidad, id_producto))
        else:
            cursor.execute("""
               UPDATE productos 
               SET stock = stock - %s 
               WHERE id_producto = %s
            """, (cantidad, id_producto))

        conexion.commit()
        cursor.close()
        conexion.close()

        return True


    @staticmethod
    def obtener_todos():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("""
        SELECT m.id_movimiento, m.tipo_movimiento, m.cantidad, m.precio_unitario, m.fecha,
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
    
    @staticmethod
    def obtener_resumen_dinero(fecha_inicio=None, fecha_fin=None):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT 
          SUM(CASE 
            WHEN tipo_movimiento = 'entrada' 
            THEN cantidad * precio_unitario 
            ELSE 0 
        END) AS invertido,

        SUM(CASE 
            WHEN tipo_movimiento = 'salida' 
            THEN cantidad * precio_unitario 
            ELSE 0 
        END) AS ganado
        FROM movimientos
        WHERE 1=1
        """

        params = []

        if fecha_inicio:
           query += " AND fecha >= %s"
           params.append(fecha_inicio)

        if fecha_fin:
           query += " AND fecha <= %s"
           params.append(fecha_fin)

        cursor.execute(query, params)
        resultado = cursor.fetchone()

        invertido = resultado['invertido'] or 0
        ganado = resultado['ganado'] or 0

        resumen = {
            "invertido": invertido,
            "ganado": ganado,
            "balance": ganado - invertido
        }

        cursor.close()
        conexion.close()

        return resumen

    @staticmethod
    def obtener_filtrado(fecha_inicio=None, fecha_fin=None, tipo=None, producto=None):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT m.*, p.nombre AS producto, u.nombre AS usuario
        FROM movimientos m
        INNER JOIN productos p ON m.id_producto = p.id_producto
        INNER JOIN usuarios u ON m.id_usuario = u.id_usuario
        WHERE 1=1
        """

        params = []

        if fecha_inicio:
           query += " AND m.fecha >= %s"
           params.append(fecha_inicio)

        if fecha_fin:
           query += " AND m.fecha <= %s"
           params.append(fecha_fin)

        if tipo:
           query += " AND m.tipo_movimiento = %s"
           params.append(tipo)

        if producto:
           query += " AND p.nombre LIKE %s"
           params.append(f"%{producto}%")

        query += " ORDER BY m.fecha DESC"

        cursor.execute(query, params)
        datos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return datos  

    @staticmethod
    def obtener_metricas(fecha_inicio=None, fecha_fin=None):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT 
            COUNT(*) as total_movimientos,
            SUM(CASE WHEN tipo_movimiento='salida' THEN cantidad ELSE 0 END) as total_ventas
        FROM movimientos
        WHERE 1=1
        """

        params = []

        if fecha_inicio:
          query += " AND fecha >= %s"
          params.append(fecha_inicio)

        if fecha_fin:
           query += " AND fecha <= %s"
           params.append(fecha_fin)

        cursor.execute(query, params)
        data = cursor.fetchone()

        cursor.close()
        conexion.close()

        return data   

    @staticmethod
    def obtener_datos_grafica(fecha_inicio=None, fecha_fin=None):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        query = """
        SELECT DATE(fecha) as fecha,
           SUM(CASE WHEN tipo_movimiento='salida' THEN cantidad * precio_unitario ELSE 0 END) as ingresos,
           SUM(CASE WHEN tipo_movimiento='entrada' THEN cantidad * precio_unitario ELSE 0 END) as gastos
        FROM movimientos
        WHERE 1=1
        """

        params = []

        if fecha_inicio:
           query += " AND fecha >= %s"
           params.append(fecha_inicio)

        if fecha_fin:
           query += " AND fecha <= %s"
           params.append(fecha_fin)

        query += " GROUP BY DATE(fecha)"

        cursor.execute(query, params)
        datos = cursor.fetchall()

        cursor.close()
        conexion.close()

        return datos 

    @staticmethod
    def obtener_alertas():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT nombre, stock FROM productos WHERE stock < 5")
        bajos = cursor.fetchall()

        cursor.close()
        conexion.close()

        alertas = []

        for p in bajos:
            alertas.append(f"Stock bajo: {p['nombre']} ({p['stock']})")

        return alertas
