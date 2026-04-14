from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario import Usuario
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.log import Log

auth_bp = Blueprint('auth', __name__)

# Mostrar login
@auth_bp.route('/login')
def login():
    return render_template('login.html')

# Procesar login
@auth_bp.route('/login', methods=['POST'])
def login_post():

    email = request.form['email']
    password = request.form['password']

    usuario = Usuario.obtener_por_email(email)

    if usuario and usuario['password'] == password:
        session['usuario'] = usuario
        Log.registrar(usuario['id_usuario'], 
              f"[AUTH] Inicio de sesión - {usuario['email']}")
        return redirect(url_for('auth.dashboard'))
    else:
        Log.registrar(0, 
              f"[AUTH] Intento fallido - {email}")
        flash("Correo o contraseña incorrectos", "danger")  
        return redirect(url_for('auth.login'))

# Dashboard según rol
@auth_bp.route('/dashboard')
def dashboard():

    if 'usuario' not in session:
        return redirect(url_for('auth.login'))

    usuario = session['usuario']

    return render_template('dashboard.html', usuario=usuario)

# Logout
@auth_bp.route('/logout')
def logout():
    id_usuario = session['usuario']['id_usuario']
    Log.registrar(id_usuario, 
              "[AUTH] Cierre de sesión")
    session.clear()
    return redirect(url_for('auth.login'))