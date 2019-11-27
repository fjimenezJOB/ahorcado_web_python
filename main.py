'''
    Sesiones en pyyhon Flask
    La gestión que hace flask en las sesiones es no utilizar espacios de memoria sino que utiliza cookies.
    Para crear la cookie y encrpitarla necesitamos una clave secreta
'''
from flask import Flask, redirect, render_template, request, session

from libreria.ahorcado import Ahorcado
from libreria.conexion import Conexion

app = Flask(__name__)
app.secret_key = 'clave_secreta'
base_datos = Conexion('localhost', 'fran', 'Hello1234', 'practica_sesiones')
player = Ahorcado()


@app.route('/')
def inicio():
    """
        Redirecciona al index(Donde se escoge si se va al login o se registra.)
    """
    return redirect('index')


@app.route('/index')
def index():
    """
        Comprueba si hay una sesion habierta:
        sesion si-> redirecciona a home.html
        sesion no -> Redirecciona al index
    """
    if session:
        session['inicio'] = True
        session['palabra'] = player.palabra_aleatoria()
        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    """
        Registra usuarios en la base de datos y comprueba que ese usuario no este.
    """
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        apellido1 = request.form.get('apellido1')
        apellido2 = request.form.get('apellido2')
        email = request.form.get('email')
        password = request.form.get('contra')
        query = f'SELECT email FROM usuarios WHERE email = "{email}"'
        existe = base_datos.query(query)
        tel = request.form.get('tel')
        if existe != ():
            error = True
            return render_template('registro.html', error=error)
        else:
            rq = f'''INSERT INTO usuarios ( nombre, apellido_1, apellido_2, telefono, email, password)
            VALUES 
            ("{nombre}","{apellido1}","{apellido2}","{tel}","{email}","{password}")'''
            base_datos.query(rq)
            return redirect('login')
    return render_template('registro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Comprueba si los usuarios estan registrados, si lo estan y introducen bien
        la contraseña les deja pasar.
        Si hay un error en la contraseña avisa al usuario que la contraseña esta mal.
        Si no esta el usuario en la base de datos se le pide que se registre.
        Introduce las variables del usuario en session.
    """
    if request.method == 'POST':
        email = request.form.get('email')
        contra = request.form.get('contra')
        query = f'SELECT nombre, password, nombre, apellido_1, apellido_2, activo FROM usuarios WHERE email = "{email}"'
        usuario = base_datos.query(query)
        if usuario != ():
            if contra == usuario[0][1] and usuario[0][5] == 1:
                session['nombre'] = usuario[0][2] + ' ' + usuario[0][3]
                session['email'] = email
                session['palabra'] = player.palabra_aleatoria()
                return redirect('home')
            else:
                error = True
                return render_template('login.html', error=error)
        else:
            no_registrado = True
            return render_template('login.html', no_registrado=no_registrado)
    return render_template('login.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    """
        Comprueba si hay una sesion abierta, si no la hay redirecciona a index.
    """
    if session:
        if request.method == 'POST':
            palabra = session['palabra']
            print(palabra)
            letra = request.form.get('letra').upper()
            player.inicio(palabra, letra)
            return render_template('home.html')
        else:
            return redirect('index')


@app.route('/salir')
def salir():
    session.clear()
    return redirect('index')


@app.route('/seguro')
def seguro():
    return render_template('desactivar.html')


@app.route('/desactivar')
def desactivar():
    email = session['email']
    session.clear()
    query = f'UPDATE usuarios SET activo = 0 WHERE email = "{email}"'
    eliminar = base_datos.query(query)
    return redirect('index')


if __name__ == "__main__":
    app.run('0.0.0.0', 5000, debug=True)
