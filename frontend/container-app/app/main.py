#
# frontend/container-app/app/main.py
#

import os

from flask import Flask, flash as flask_flash, render_template
from flask import request, make_response, url_for, redirect, session
from flask_wtf.csrf import CSRFProtect, CSRFError

from modules.motando_forms import LoginForm
from modules.motando_authcookie import MotandoAuthCookie
from modules.motando_usuario import UsuarioParticular
from modules import motando_utils

#
# Globals
#
AUTH_COOKIE_NAME = os.environ.get('MOTANDO_AUTH_COOKIE_NAME')

#
# Flask initialization
#
app = Flask(__name__)
app.config['SECRET_KEY'] = motando_utils.get_csrf_secretkey()
    

# Session
app.config['SESSION_COOKIE_NAME'] = 'XxMotandoXxSession'
app.config['SESSION_COOKIE_DOMAIN'] = 'motando.ocibook.com.br'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# CSRF Protection
csrf = CSRFProtect()
csrf.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/form/login', methods=['GET', 'POST'])
def login():   
    global AUTH_COOKIE_NAME

    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():      
           email = request.form.get('email')
           senha = request.form.get('senha') 
                      
           jwt = motando_utils.auth_service(email=email, senha=senha)
           
           if jwt.get('code') == 200:
               jwt_token = jwt['data']['access_token']

               auth_cookie = MotandoAuthCookie()

               auth_cookie.email = email
               auth_cookie.jwt_token = jwt_token
               
               cookie_value = auth_cookie.create()

               # TODO: implementar lógica para redirecionar 'admin_lojista'
               resp = make_response(redirect(url_for('admin_particular')))

               resp.set_cookie(key=AUTH_COOKIE_NAME, value=cookie_value, secure=True, 
                   max_age=3600, httponly=True, samesite='Strict', domain='motando.ocibook.com.br')
           
               # TODO: implementar registro de LAST LOGIN

               return resp

           else:
               flask_flash(u'Usuário ou senha inválido(s).', 'error')

        else:
            flask_flash(u'Erro ao realizar Login!', 'error')

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    resp = make_response(redirect(url_for('home')))

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')

    if cookie_value:
        auth_cookie = MotandoAuthCookie()

        auth_cookie.remove(cookie_value)    

        resp.set_cookie(key=AUTH_COOKIE_NAME, value='', secure=True, httponly=True, 
            expires=0, samesite='Strict', domain='motando.ocibook.com.br')
        
    session.clear()
    
    return resp


@app.route('/novo/particular-lojista', methods=['GET'])
def usuario_particular_logista():
    return render_template('usuario_particular_logista.html')


@app.route('/form/particular', methods=['GET'])
def form_particular():
    return render_template('form_particular.html')


@app.route('/form/lojista', methods=['GET'])
def form_lojista():
    return render_template('form_lojista.html')


@app.route('/usuario/particular/confirmacao')
def confirm():
    return render_template('email_confirmacao.html')


@app.route('/admin/usuario/particular')
@motando_utils.ensure_logged_in
def admin_particular():
    global AUTH_COOKIE_NAME

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')
    
    auth_cookie = MotandoAuthCookie()    
    jwt_token = auth_cookie.get_jwt(cookie_value)

    usuario_particular = UsuarioParticular()    
    profile = usuario_particular.get_profile(jwt_token)

    if profile.get('code') == 200:
        return render_template('admin_particular/home.html', profile=profile)
    else:
        return render_template('404.html')


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400