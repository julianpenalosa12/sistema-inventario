from flask import Blueprint, render_template, request, redirect, url_for, session
from models.usuario import Usuario
from flask import Blueprint, render_template, request, redirect, url_for, session, flash

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
        return redirect(url_for('auth.dashboard'))
    else:
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
    session.clear()
    return redirect(url_for('auth.login'))