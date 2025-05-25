from flask import Flask, render_template, request, send_file
from datetime import datetime
import csv
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return render_template(
        'code.html')  # Solo muestra la página principal, sin el menú

# Ruta para el menú
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    from datetime import datetime   

    # Obtener el día de la semana (0 = Lunes, 6 = Domingo)
    #dia_actual = datetime.now().weekday() 
    dia_actual =0
    # Si es fin de semana (5=Sábado, 6=Domingo)
    if dia_actual >= 5:
        return render_template('code.html', menu_items=None, mensaje="Lo sentimos, solo atendemos de lunes a viernes.")

    # Menú para cada día de la semana
    menus_semanales = {
        0: [  # Lunes
            {"name": "Lunes Opción 1", "description": "Seco con Frejoles", "precio": 11, "image": "lunes1.png"},
            {"name": "Lunes Opción 2", "description": "Tallarines verdes con pollo a la olla", "precio": 11, "image": "lunes2.png"}
        ],
        1: [  # Martes
            {"name": "Martes Opción 1", "description": "Chicharron de pollo con papas y arroz", "precio": 11, "image": "martes1.png"},
            {"name": "Martes Opción 2", "description": "Ensalada rusa con milanesa", "precio": 11, "image": "martes2.png"}
        ],
        2: [  # Miércoles
            {"name": "Miércoles Opción 1", "description": "Arroz Chaufa con cecina", "precio": 11, "image": "miercoles1.png"},
            {"name": "Miércoles Opción 2", "description": "Macarrones con Pollo", "precio": 11, "image": "miercoles2.png"}
        ],
        3: [  # Jueves
            {"name": "Jueves Opción 1", "description": "Tallarines a la Bolognesa", "precio": 11, "image": "jueves1.png"},
            {"name": "Jueves Opción 2", "description": "Pachamanca a la Olla", "precio": 11, "image": "jueves2.png"}
        ],
        4: [  # Viernes
            {"name": "Viernes Opción 1", "description": "Tallarines verdes con pollo al horno y huancaina", "precio": 11, "image": "viernes1.png"},
            {"name": "Viernes Opción 2", "description": "Pure con lomo saltado", "precio": 11, "image": "viernes2.png"}
        ]
        
    }

    

    menu_items = menus_semanales[dia_actual]
    return render_template('code.html', menu_items=menu_items)


# Ruta para manejar la selección de un plato
@app.route('/seleccionar/<plato>', methods=['POST'])
def seleccionar(plato):
    # Aquí podrías agregar una lógica para confirmar la selección del plato
    return f'Has seleccionado: {plato}'


# Ruta para reservar y guardar en CSV
@app.route('/reservar/<plato>', methods=['GET', 'POST'])
def reservar(plato):
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        fecha_hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Archivo CSV para reservas
        archivo = 'reservas.csv'
        existe = os.path.isfile(archivo)
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Si no existía, escribir cabecera
            if not existe:
                writer.writerow(['Nombre', 'Correo', 'Teléfono', 'Plato', 'Fecha y Hora'])
            writer.writerow([nombre, correo, telefono, plato, fecha_hora])

        return render_template('confirmacion.html', plato=plato, nombre=nombre, correo=correo,
telefono=telefono, fecha_hora=fecha_hora)

    # Si es GET, mostrar el formulario
    return render_template('reservar.html', plato=plato)

# Ruta secreta para exportar y descargar reservas
@app.route('/exportar-reservas')
def exportar_reservas():
    archivo = 'reservas.csv'
    if os.path.exists(archivo):
        return send_file(archivo, as_attachment=True)
    return '<h3>No hay reservas registradas aún. <a href=\"/\">Volver al inicio</a></h3>'

# Panel de administración: usa plantilla admin.html
@app.route('/admin')
def admin_panel():
    return render_template('admin.html')

# Ruta para borrar el archivo de reservas y volver al panel
@app.route('/borrar-reservas')
def borrar_reservas():
    archivo = 'reservas.csv'
    if os.path.exists(archivo):
        os.remove(archivo)
        mensaje = "borrado"
    else:
        mensaje = "no_existe"
    return render_template('admin.html', mensaje=mensaje)

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


# Ejecutar la aplicación
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)