from flask import Flask, render_template, request, send_file
from datetime import datetime
import pytz
import csv
import os

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal - Página de inicio
@app.route('/')
def home():
    return render_template('code.html')  # Muestra la página principal

# Ruta para reservar - ahora incluye la funcionalidad del menú
@app.route('/reservar', methods=['GET', 'POST'])
def reservar():  

    # Obtener el día de la semana (0 = Lunes, 6 = Domingo)
    lima = pytz.timezone('America/Lima')
    dia_actual = datetime.now(lima).weekday()

    # Si es fin de semana (5=Sábado, 6=Domingo), no hay servicio
    if dia_actual >= 5:
        return render_template('reservar.html', menu_items=None, 
                             mensaje="Lo sentimos, solo atendemos de lunes a viernes.")

    # Diccionario con los menús para cada día de la semana
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

    # Obtener el menú del día actual
    menu_items = menus_semanales[dia_actual]
    return render_template('reservar.html', menu_items=menu_items)
@app.route('/menu')
def menu_semanal():
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
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
    return render_template('menu.html', menus_semanales=menus_semanales, dias=dias)
# Ruta para procesar la reserva de un plato específico
@app.route('/hacer-reserva/<plato>', methods=['GET', 'POST'])
def hacer_reserva(plato):
    # Si el usuario envía el formulario (método POST)
    if request.method == 'POST':
        # Obtener los datos del formulario y eliminar espacios en blanco
        nombre = request.form.get('nombre', '').strip()
        correo = request.form.get('correo', '').strip()
        telefono = request.form.get('telefono', '').strip()
        
        # Validación simple: verificar que todos los campos estén llenos
        if not nombre or not correo or not telefono:
            return render_template('formulario-reserva.html', plato=plato, 
                                 error="Por favor, completa todos los campos")
        
        # Obtener la fecha y hora actual para la reserva
        lima = pytz.timezone('America/Lima')
        fecha_hora = datetime.now(lima).strftime('%Y-%m-%d %H:%M:%S')

        
        # Nombre del archivo CSV donde se guardan las reservas
        archivo = 'reservas.csv'
        # Verificar si el archivo ya existe
        existe = os.path.isfile(archivo)
        
        # Abrir el archivo en modo "agregar" para no sobrescribir datos existentes
        with open(archivo, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Si es la primera reserva, crear la cabecera del CSV
            if not existe:
                writer.writerow(['Nombre', 'Correo', 'Teléfono', 'Plato', 'Fecha y Hora'])
            # Agregar la nueva reserva al archivo
            writer.writerow([nombre, correo, telefono, plato, fecha_hora])

        # Mostrar página de confirmación con los datos de la reserva
        return render_template('confirmacion.html', plato=plato, nombre=nombre, 
                             correo=correo, telefono=telefono, fecha_hora=fecha_hora)

    # Si es una petición GET, mostrar el formulario de reserva
    return render_template('formulario-reserva.html', plato=plato)

# Ruta para manejar la selección de un plato (opcional, no se usa actualmente)
@app.route('/seleccionar/<plato>', methods=['POST'])
def seleccionar(plato):
    # Función simple que confirma la selección del plato
    return f'Has seleccionado: {plato}'

# Ruta para descargar el archivo de reservas (para administradores)
@app.route('/exportar-reservas')
def exportar_reservas():
    archivo = 'reservas.csv'
    # Verificar si existe el archivo de reservas
    if os.path.exists(archivo):
        # Enviar el archivo como descarga
        return send_file(archivo, as_attachment=True)
    # Si no hay reservas, mostrar mensaje
    return '<h3>No hay reservas registradas aún. <a href="/">Volver al inicio</a></h3>'

# Ruta para el panel de administración
@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        # Verificar credenciales
        usuario = request.form.get('usuario', '').strip()
        password = request.form.get('password', '').strip()

        # Lista de usuarios autorizados y contraseña común
        USUARIOS_AUTORIZADOS = ['24200178', '24200183', '24200185', '24200152', '24200165']
        ADMIN_PASSWORD = 'aquimenu2025'

        if usuario in USUARIOS_AUTORIZADOS and password == ADMIN_PASSWORD:
            # Login exitoso, mostrar panel de admin
            return render_template('admin.html', admin_name=usuario)
        else:
            # Login fallido, mostrar error
            return render_template('admin-login.html', error="Usuario o contraseña incorrectos")

    # Si es GET, mostrar formulario de login
    return render_template('admin-login.html')

# Ruta para borrar todas las reservas (para administradores)
@app.route('/borrar-reservas')
def borrar_reservas():
    archivo = 'reservas.csv'
    # Verificar si existe el archivo
    if os.path.exists(archivo):
        # Eliminar el archivo de reservas
        os.remove(archivo)
        mensaje = "borrado"
    else:
        mensaje = "no_existe"
    # Volver al panel de admin con un mensaje de confirmación
    return render_template('admin.html', mensaje=mensaje)

# Ruta para la página "Nosotros"
@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

# Ejecutar la aplicación Flask
if __name__ == '__main__':
    # Obtener el puerto desde las variables de entorno o usar 3000 por defecto
    port = int(os.environ.get("PORT", 3000))
    # Iniciar el servidor Flask
    app.run(host="0.0.0.0", port=port, debug=True)