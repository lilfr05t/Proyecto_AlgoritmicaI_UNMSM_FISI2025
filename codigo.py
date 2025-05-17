from flask import Flask, render_template, request

# Crear la aplicación Flask
app = Flask(__name__)

# Ruta principal
@app.route('/')
def home():
    return render_template('code.html')  # Solo muestra la página principal, sin el menú

# Ruta para el menú
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    menu_items = [
        {"name": "OPCION 1", 
         "description": "Descripción del plato 1", 
         "price": 11, 
         "image": "plato1.png"},  # Imagen PNG para opción 1
        {"name": "OPCION 2", 
         "description": "Descripción del plato 2", 
         "price": 12, 
         "image": "plato2.png"},  # Imagen PNG para opción 2
    ]
    return render_template('code.html', menu_items=menu_items)  # Muestra el menú solo en /menu

# Ruta para manejar la selección de un plato
@app.route('/seleccionar/<plato>', methods=['POST'])
def seleccionar(plato):
    # Aquí podrías agregar una lógica para confirmar la selección del plato
    return f'Has seleccionado: {plato}'

# Ejecutar la aplicación
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
