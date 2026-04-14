from flask import Blueprint, render_template, request, redirect, url_for, session
from models.movimiento import Movimiento
from models.producto import Producto
from models.log import Log  

movimiento_bp = Blueprint('movimientos', __name__)


# LISTAR
@movimiento_bp.route('/movimientos')
def listar_movimientos():

    if "usuario" not in session:
        return redirect("/login")

    movimientos = Movimiento.obtener_todos()
    productos = Producto.obtener_todos()

    return render_template("movimientos.html",
                           movimientos=movimientos,
                           productos=productos)


# CREAR
@movimiento_bp.route('/movimientos/crear', methods=['POST'])
def crear_movimiento():

    id_producto = request.form['id_producto']
    tipo = request.form['tipo']
    cantidad = int(request.form['cantidad'])
    id_usuario = session["usuario"]["id_usuario"]

    resultado = Movimiento.crear(id_producto, tipo, cantidad, id_usuario)
    producto = Producto.obtener_por_id(id_producto)
    nombre_producto = producto['nombre']
    print("DEBUG:", nombre_producto)  

    if resultado == False:
       Log.registrar(id_usuario, 
           f"[MOVIMIENTOS] ERROR intento de {tipo} mayor al stock (Producto: {nombre_producto})")
    else:
       Log.registrar(id_usuario, 
           f"[MOVIMIENTOS] {tipo.upper()} de {cantidad} unidades (Producto: {nombre_producto})")

    return redirect(url_for('movimientos.listar_movimientos'))