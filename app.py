from flask import Flask
from routes.usuario_routes import usuario_bp
from routes.auth_routes import auth_bp
from flask import session, redirect
from routes.categoria_routes import categoria_bp
from routes.producto_routes import producto_bp

app = Flask(__name__)

app.secret_key = "clave_secreta"

app.register_blueprint(usuario_bp)  
app.register_blueprint(auth_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(producto_bp)

@app.route("/")
def inicio():
    # Si ya está logeado → va al dashboard
    if "usuario" in session:
        return redirect("/dashboard")

    # Si NO está logeado → va al login
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)