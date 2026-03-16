from flask import Blueprint, render_template, request, redirect, url_for
from models.usuario import Usuario

usuario_bp = Blueprint('usuarios', __name__)


# LISTAR USUARIOS
@usuario_bp.route('/usuarios')
def listar_usuarios():

    usuarios = Usuario.obtener_todos()
    return render_template("usuarios.html", usuarios=usuarios)


# CREAR USUARIO
@usuario_bp.route('/usuarios/crear', methods=['POST'])
def crear_usuario():

    nombre = request.form['nombre']
    email = request.form['email']
    password = request.form['password']
    rol = request.form['rol']

    Usuario.crear(nombre, email, password, rol)

    return redirect(url_for('usuarios.listar_usuarios'))


# ACTUALIZAR USUARIO
@usuario_bp.route('/usuarios/editar/<int:id>', methods=['POST'])
def editar_usuario(id):

    nombre = request.form['nombre']
    email = request.form['email']
    rol = request.form['rol']

    Usuario.actualizar(id, nombre, email, rol)

    return redirect(url_for('usuarios.listar_usuarios'))


# ELIMINAR USUARIO
@usuario_bp.route('/usuarios/eliminar/<int:id>')
def eliminar_usuario(id):

    Usuario.eliminar(id)

    return redirect(url_for('usuarios.listar_usuarios'))

    # MOSTRAR FORMULARIO DE EDICIÓN
@usuario_bp.route('/usuarios/editar/<int:id>')
def mostrar_editar_usuario(id):

    usuario = Usuario.obtener_por_id(id)

    return render_template("editar_usuario.html", usuario=usuario)


# GUARDAR CAMBIOS
@usuario_bp.route('/usuarios/actualizar/<int:id>', methods=['POST'])
def actualizar_usuario(id):

    nombre = request.form['nombre']
    email = request.form['email']
    rol = request.form['rol']

    Usuario.actualizar(id, nombre, email, rol)

    return redirect(url_for('usuarios.listar_usuarios'))