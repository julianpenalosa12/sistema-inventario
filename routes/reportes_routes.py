from flask import Blueprint, render_template, request, session, redirect
from models.movimiento import Movimiento
import pandas as pd
from flask import send_file

reporte_bp = Blueprint('reportes', __name__)
@reporte_bp.route('/reportes', methods=['GET'])
def ver_reportes():

    if "usuario" not in session:
        return redirect("/login")

    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    tipo = request.args.get('tipo')
    producto = request.args.get('producto')

    # 📊 Movimientos filtrados
    movimientos = Movimiento.obtener_filtrado(fecha_inicio, fecha_fin, tipo, producto)

    # 💰 Resumen financiero
    resumen = Movimiento.obtener_resumen_dinero(fecha_inicio, fecha_fin)

    # 📈 Datos gráfica
    grafica = Movimiento.obtener_datos_grafica(fecha_inicio, fecha_fin)

    # 📊 Métricas
    metricas = Movimiento.obtener_metricas(fecha_inicio, fecha_fin)

    # ⚠️ Alertas
    alertas = Movimiento.obtener_alertas()

    return render_template("reportes.html",
                           movimientos=movimientos,
                           resumen=resumen,
                           grafica=grafica,
                           metricas=metricas,
                           alertas=alertas,
                           usuario=session['usuario'])

@reporte_bp.route('/reportes/exportar')
def exportar():

    movimientos = Movimiento.obtener_filtrado()

    df = pd.DataFrame(movimientos)

    archivo = "reporte.xlsx"
    df.to_excel(archivo, index=False)

    return send_file(archivo, as_attachment=True)