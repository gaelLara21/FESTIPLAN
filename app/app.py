from flask import Flask, render_template 

app=Flask(__name__)

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


if __name__=='__main__':
    app.run(debug=True, port=5000)