import mysql.connector
from config import db_config

class Usuario:

    @staticmethod
    def obtener_todos():
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        cursor.close()
        conexion.close()

        return usuarios


    @staticmethod
    def crear(nombre, email, password, rol):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        INSERT INTO usuarios (nombre, email, password, rol)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(sql, (nombre, email, password, rol))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def actualizar(id_usuario, nombre, email, rol):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        sql = """
        UPDATE usuarios
        SET nombre=%s, email=%s, rol=%s
        WHERE id_usuario=%s
        """

        cursor.execute(sql, (nombre, email, rol, id_usuario))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def eliminar(id_usuario):
        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor()

        cursor.execute("DELETE FROM usuarios WHERE id_usuario=%s", (id_usuario,))
        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def obtener_por_id(id_usuario):

        conexion = mysql.connector.connect(**db_config)
        cursor = conexion.cursor(dictionary=True)

        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        usuario = cursor.fetchone()

        cursor.close()  
        conexion.close()

        return usuario
    
    @staticmethod
    def obtener_por_email(email):

       conexion = mysql.connector.connect(**db_config)
       cursor = conexion.cursor(dictionary=True)

       cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
       usuario = cursor.fetchone()

       cursor.close()
       conexion.close()

       return usuario