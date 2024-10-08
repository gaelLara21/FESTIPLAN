from flask import Flask, render_template 

app=Flask(__name__)

###################### Rutas conectadas a base de Datos ######################################
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup ():
    return render_template('signup.html')

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


@app.route('/qr')
def qr():
    return render_template('qr.html')

############################ Terminan rutas ordinarias ###################################################


if __name__=='__main__':
    app.run(debug=True, port=5000)