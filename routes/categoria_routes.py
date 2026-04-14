from flask import Blueprint, render_template, request, redirect, url_for
from models.categoria import Categoria
from models.log import Log
from flask import session

categoria_bp = Blueprint('categorias', __name__)

# LISTAR
@categoria_bp.route('/categorias')
def listar_categorias():
    categorias = Categoria.obtener_todas()
    return render_template("categorias.html", categorias=categorias)

# CREAR
@categoria_bp.route('/categorias/crear', methods=['POST'])
def crear_categoria():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']   

    Categoria.crear(nombre, descripcion)
    Log.registrar(session['usuario']['id_usuario'], 
                  f"[CATEGORIAS] Creó categoría {nombre}")
    return redirect(url_for('categorias.listar_categorias'))

# ELIMINAR
@categoria_bp.route('/categorias/eliminar/<int:id>')
def eliminar_categoria(id):
    Categoria.eliminar(id)
    Log.registrar(session['usuario']['id_usuario'], 
                  f"[CATEGORIAS] Eliminó categoría ID {id}")
    return redirect(url_for('categorias.listar_categorias'))

# MOSTRAR EDITAR
@categoria_bp.route('/categorias/editar/<int:id>')
def mostrar_editar_categoria(id):
    categoria = Categoria.obtener_por_id(id)
    return render_template("editar_categoria.html", categoria=categoria)

# ACTUALIZAR
@categoria_bp.route('/categorias/actualizar/<int:id>', methods=['POST'])
def actualizar_categoria(id):
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']

    Categoria.actualizar(id, nombre, descripcion)

    Log.registrar(session['usuario']['id_usuario'], 
                  f"[CATEGORIAS] Editó categoría ID {id}")

    return redirect(url_for('categorias.listar_categorias'))