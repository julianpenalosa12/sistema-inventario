from flask import Blueprint, render_template
from models.log import Log

log_bp = Blueprint('logs', __name__)

@log_bp.route('/logs')
def ver_logs():
    logs = Log.obtener_todos()
    return render_template("logs.html", logs=logs)