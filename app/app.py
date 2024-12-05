from flask import Flask, redirect, render_template, request, url_for, flash, session, send_file, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
from datetime import datetime
import qrcode
from io import BytesIO
import base64
import openai

app=Flask(__name__)
app.secret_key = 'supersecreto'

# Conexión a la base de datos

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Gael2122LaraB_",
    database="festyplan"
)
cursor = db.cursor(dictionary=True)


############# Ruta del ChatBot ##################



############# Termina Ruta del ChatBot ##################

###################### Rutas conectadas a base de Datos ######################################

@app.route('/mis_boletos')
def mis_boletos():
    if 'user_id' not in session:
        flash("Debes iniciar sesión para ver tus boletos", "error")
        return redirect(url_for('index'))

    user_id = session['user_id']
    cursor.execute("""
        SELECT b.id_boleto, e.titulo, e.fecha, e.costo, b.qr_code 
        FROM boletos b
        INNER JOIN eventos e ON b.id_evento = e.id_evento
        WHERE b.id_user = %s
    """, (user_id,))
    boletos = cursor.fetchall()

    return render_template('mis_boletos.html', boletos=boletos)


@app.route('/venta/<int:id_evento>', methods=['GET', 'POST'])
def venta(id_evento):
    if 'user_id' not in session:
        flash("Debes iniciar sesión para comprar boletos", "error")
        return redirect(url_for('index'))
    
    # Obtener información del evento
    cursor.execute("""
        SELECT id_evento, titulo, descripcion, fecha, capacidad, costo, 
               CONCAT('/', foto) AS foto
        FROM eventos WHERE id_evento = %s
    """, (id_evento,))
    evento = cursor.fetchone()

    if not evento:
        flash("El evento no existe", "error")
        return redirect(url_for('eventos'))

    if request.method == 'POST':
        cantidad = int(request.form['cantidad'])
        total = cantidad * evento['costo']
        user_id = session['user_id']

        # Validar capacidad
        if cantidad > evento['capacidad']:
            flash("No hay suficientes boletos disponibles", "error")
            return redirect(url_for('venta', id_evento=id_evento))

        # Si el costo es 0, generar QR directamente
        if evento['costo'] == 0:
            # Generar código QR único para la transacción
            datos_transaccion = f"Evento: {evento['titulo']}\nUsuario: {user_id}\nCantidad: {cantidad}\nTotal: {total}"
            qr = qrcode.make(datos_transaccion)
            qr_filename = f"static/qrs/qr_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
            qr.save(qr_filename)

            # Insertar boletos en la base de datos
            cursor.execute("""
                INSERT INTO boletos (id_user, id_evento, cantidad, qr_code) VALUES (%s, %s, %s, %s)
            """, (user_id, id_evento, cantidad, qr_filename))
            db.commit()

            # Actualizar capacidad restante del evento
            nueva_capacidad = evento['capacidad'] - cantidad
            cursor.execute("UPDATE eventos SET capacidad = %s WHERE id_evento = %s", (nueva_capacidad, id_evento))
            db.commit()

            flash("Compra realizada con éxito", "success")
            return redirect(url_for('mis_boletos'))
        
        # Si el costo es mayor a 0, redirigir a página de pago
        else:
            return redirect(url_for('pay', id_evento=id_evento, cantidad=cantidad))

    return render_template('venta.html', evento=evento)

##################### Terminan Rutas Conectadas a una base de Datos ###############################



###################### Rutas Para inicio de sesión ######################################

@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']

        #Validar si el correo ingresado ya es existente
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash('Este Correo ya existe', 'error')
            return redirect(url_for('index'))
        
        #Encriptación de contraseñas
        hashed_pasword = generate_password_hash(password)

        #Insertar el Nuevo Usuario en la base de datos
        sql = "INSERT INTO user (name, lastname, email, password) VALUES (%s, %s, %s, %s)"
        val = (name, lastname, email, hashed_pasword)
        cursor.execute(sql, val)
        db.commit()

        flash ('Usuario Registrado Correctamente', 'success')
        return redirect(url_for('index'))
    
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        #Buscar al usuario en la base de datos

        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            # Establecer las variables de sesión
            session['user_id'] = user['id_user']
            session['user_name'] = user['name']  # Opcional: guardar el nombre del usuario
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo o contraseña incorrectos', 'error')
            return redirect(url_for('index'))

@app.route('/logout')
def logout():
    # Cerrar sesión y eliminar los datos del usuario de la sesión
    session.pop('user_id', None)
    session.pop('user_name', None)  # Eliminar el nombre del usuario de la sesión
    flash('Has cerrado sesión', 'success')
    return redirect(url_for('index'))

###################### Terminan Rutas Para inicio de sesión ######################################


###################### Rutas Ordinarias ##################################################
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/aviso')
def aviso():
    return render_template('aviso.html')

@app.route('/pago/<int:id_evento>/<int:cantidad>', methods=['GET', 'POST'])
def pay(id_evento, cantidad):
    # Obtener detalles del evento
    cursor.execute("SELECT titulo, costo FROM eventos WHERE id_evento = %s", (id_evento,))
    evento = cursor.fetchone()
    
    total = evento['costo'] * cantidad
    
    return render_template('pay.html', evento=evento, cantidad=cantidad, total=total)

############# Rutas de los eventos ##################

@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash("Debes iniciar sesión para crear un evento", "error")
            return redirect(url_for('index'))

        # Obtener datos del formulario
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        capacidad = request.form['capacidad']
        costo = request.form['costo']
        categoria = request.form['categoria']
        user_id = session['user_id']

        # Manejo de la imagen
        if 'foto' not in request.files:
            flash('No se subió ninguna imagen', 'error')
            return redirect(url_for('crear'))
        
        foto = request.files['foto']
        
        # Validar que se haya seleccionado una imagen
        if foto.filename == '':
            flash('No se seleccionó ninguna imagen', 'error')
            return redirect(url_for('crear'))
        
        # Guardar la imagen en el servidor
        foto_filename = secure_filename(foto.filename)
        foto_path = os.path.join('static/uploads', foto_filename)
        foto.save(foto_path)

        # Insertar el evento en la base de datos
        sql = """
            INSERT INTO eventos (titulo, descripcion, capacidad, costo, categoria, foto, fecha, id_user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        val = (titulo, descripcion, capacidad, costo, categoria, foto_path, fecha, user_id)
        cursor.execute(sql, val)
        db.commit()

        flash('Evento creado correctamente', 'success')
        return redirect(url_for('index'))

    return render_template('crear.html')

# Otras rutas y funciones de la aplicación
@app.route('/eventos')
def eventos():
    cursor.execute("SELECT * FROM eventos")
    eventos = cursor.fetchall()
    return render_template('eventos.html', eventos=eventos)

@app.route('/mis_eventos')
def mis_eventos():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute("SELECT * FROM eventos WHERE id_user = %s", (user_id,))
        eventos = cursor.fetchall()

        # Crear una lista de eventos con datos necesarios
        eventos_lista = [{"titulo": evento[1], "fecha": evento[6], "id_evento": evento[0]} for evento in eventos]

        # Si se hace una petición JSON, respondemos con los datos en formato JSON
        if request.is_xhr:
            return jsonify(eventos_lista)
        else:
            return render_template('mis_eventos.html', eventos=eventos)
    else:
        return redirect(url_for('index'))

@app.route('/eliminar_evento/<int:id_evento>', methods=['POST'])
def eliminar_evento(id_evento):
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute("DELETE FROM eventos WHERE id_evento = %s AND id_user = %s", (id_evento, user_id))
        db.commit()
        flash("Evento eliminado correctamente", "success")
    else:
        flash("Debes iniciar sesión para realizar esta acción", "error")
    return redirect(url_for('mis_eventos'))

@app.route('/editar_evento/<int:id_evento>', methods=['GET', 'POST'])
def editar_evento(id_evento):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    user_id = session['user_id']

    # Obtener los detalles del evento
    cursor.execute("SELECT * FROM eventos WHERE id_evento = %s AND id_user = %s", (id_evento, user_id))
    evento = cursor.fetchone()

    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        fecha = request.form['fecha']
        capacidad = request.form['capacidad']
        costo = request.form['costo']
        categoria = request.form['categoria']

        # Actualizar el evento en la base de datos
        cursor.execute("""
            UPDATE eventos 
            SET titulo = %s, descripcion = %s, fecha = %s, capacidad = %s, costo = %s, categoria = %s 
            WHERE id_evento = %s AND id_user = %s
        """, (titulo, descripcion, fecha, capacidad, costo, categoria, id_evento, user_id))
        db.commit()
        flash("Evento actualizado correctamente", "success")
        return redirect(url_for('mis_eventos'))

    return render_template('editar_evento.html', evento=evento)
    
######## Terminan Rutas de los Eventos ################
    

############################ Terminan rutas ordinarias ###################################################


if __name__=='__main__':
    app.run(debug=True, port=5000)