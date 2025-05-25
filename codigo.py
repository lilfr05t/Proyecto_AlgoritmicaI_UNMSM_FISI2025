from flask import Flask, render_template, request

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
    dia_actual = datetime.now().weekday()

    # Si es fin de semana (5=Sábado, 6=Domingo)
    if dia_actual >= 5:
        return render_template('code.html', menu_items=None, mensaje="Lo sentimos, solo atendemos de lunes a viernes.")

    # Menú para cada día de la semana
    menus_semanales = {
        0: [  # Lunes
            {"name": "Lunes Opción 1", "description": "Pasta Carbonara", "price": 11, "image": "lunes1.png"},
            {"name": "Lunes Opción 2", "description": "Ensalada César", "price": 11, "image": "lunes2.png"}
        ],
        1: [  # Martes
            {"name": "Martes Opción 1", "description": "Pollo al Curry", "price": 11, "image": "plato1.png"},
            {"name": "Martes Opción 2", "description": "Risotto de Champiñones", "price": 11, "image": "plato2.png"}
        ],
        2: [  # Miércoles
            {"name": "Miércoles Opción 1", "description": "Pescado a la Plancha", "price": 11, "image": "plato1.png"},
            {"name": "Miércoles Opción 2", "description": "Lasaña Vegetariana", "price": 11, "image": "plato2.png"}
        ],
        3: [  # Jueves
            {"name": "Jueves Opción 1", "description": "Paella de Mariscos", "price": 11, "image": "plato1.png"},
            {"name": "Jueves Opción 2", "description": "Hamburguesa Gourmet", "price": 11, "image": "plato2.png"}
        ],
        4: [  # Viernes
            {"name": "Viernes Opción 1", "description": "Salmón al Horno", "price": 11, "image": "plato1.png"},
            {"name": "Viernes Opción 2", "description": "Pizza Artesanal", "price": 11, "image": "plato2.png"}
        ]
    }

    menu_items = menus_semanales[dia_actual]
    return render_template('code.html', menu_items=menu_items)


# Ruta para manejar la selección de un plato
@app.route('/seleccionar/<plato>', methods=['POST'])
def seleccionar(plato):
    # Aquí podrías agregar una lógica para confirmar la selección del plato
    return f'Has seleccionado: {plato}'


@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')


# Ejecutar la aplicación
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port, debug=True)