from flask import Blueprint, render_template, request, redirect, url_for
from models.producto import Producto
from models.categoria import Categoria

producto_bp = Blueprint('productos', __name__)

# CREAR
@producto_bp.route('/productos/crear', methods=['POST'])
def crear_producto():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    id_categoria = request.form['id_categoria']

    Producto.crear(nombre, descripcion, precio, stock, id_categoria)
    return redirect(url_for('productos.listar_productos'))


# ELIMINAR
@producto_bp.route('/productos/eliminar/<int:id>')
def eliminar_producto(id):
    Producto.eliminar(id)
    return redirect(url_for('productos.listar_productos'))


# EDITAR (mostrar)
@producto_bp.route('/productos/editar/<int:id>')
def mostrar_editar_producto(id):
    producto = Producto.obtener_por_id(id)
    categorias = Categoria.obtener_todas()

    return render_template("editar_producto.html", producto=producto, categorias=categorias)


# ACTUALIZAR
@producto_bp.route('/productos/actualizar/<int:id>', methods=['POST'])
def actualizar_producto(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    stock = request.form['stock']
    id_categoria = request.form['id_categoria']

    Producto.actualizar(id, nombre, descripcion, precio, stock, id_categoria)
    return redirect(url_for('productos.listar_productos'))

@producto_bp.route('/productos')
def listar_productos():

    buscar = request.args.get('buscar')

    if buscar:
        productos = Producto.buscar(buscar)
    else:
        productos = Producto.obtener_todos()

    categorias = Categoria.obtener_todas()

    return render_template("productos.html",
                           productos=productos,
                           categorias=categorias)