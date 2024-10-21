from flask import Flask, redirect, render_template, request, url_for, flash, session
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

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

###################### Rutas conectadas a base de Datos ######################################

@app.route('/boletos')
def boletos():
    return render_template('boletos.html')

@app.route('/crear')
def crear():
    return render_template('crear.html')

@app.route('/venta')
def venta():
    return render_template('venta.html')

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
            session['user_id'] = user['id_user']
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

@app.route('/galeria')
def galeria():
    return render_template('galeria.html')

@app.route('/eventos')
def eventos():
    return render_template('eventos.html')

@app.route('/mis_eventos')
def mis_eventos():
    if 'user_id' in session:
        return render_template('mis_eventos.html')
    else:
        return redirect(url_for('index'))  
    
    
@app.route('/mis_boletos')
def mis_boletos():
    if 'user_id' in session:
        # Lógica para mostrar los boletos del usuario
        return render_template('mis_boletos.html')
    else:
        return redirect(url_for('index'))  # Redirigir si no está logueado
############################ Terminan rutas ordinarias ###################################################


if __name__=='__main__':
    app.run(debug=True, port=5000)