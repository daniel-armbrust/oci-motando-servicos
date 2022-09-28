#
# frontend/container-app/app/main.py
#

import os

from flask import Flask, flash as flask_flash, render_template
from flask import request, make_response, url_for, redirect, session
from flask_wtf.csrf import CSRFProtect, CSRFError

from modules.motando_forms import LoginForm, CadastroUsuarioParticularForm, AnuncioForm
from modules.motando_authcookie import MotandoAuthCookie
from modules.motando_usuario import MotandoUsuarioParticular
from modules.motando_anuncio import MotandoAnuncio
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
           
           if jwt.get('status') == 'success':
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


@app.route('/form/particular', methods=['GET', 'POST'])
def form_particular():
    """Formulário para cadastro de um Novo Usuário Particular.
    
    """
    form = CadastroUsuarioParticularForm()

    if request.method == 'POST':
        brasil_estado_id = form.data.get('brasil_estado')
        brasil_cidade_id = form.data.get('brasil_cidade')

        form.brasil_estado.choices = [(brasil_estado_id, brasil_estado_id,)]
        form.brasil_cidade.choices = [(brasil_cidade_id, brasil_cidade_id,)]

        if form.validate_on_submit():                        
            usuario_particular = MotandoUsuarioParticular()
            resp = usuario_particular.add(form.data)

            status = resp.get('status')

            if status == 'success':
                return redirect(url_for('confirm'))      
            elif status == 'fail':
                flask_flash(u'Erro ao realizar o novo cadastro. O e-mail informado já existe.', 'error')
            else:
                flask_flash(u'Erro ao realizar o novo cadastro. Por favor, tente novamente mais tarde.', 'error')
            
        else:
            flask_flash(u'Erro ao cadastrar novos dados. Por favor, corrigir os dados do formuládio.', 'error')

    return render_template('form_particular.html', form=form)


@app.route('/form/lojista', methods=['GET'])
def form_lojista():
    return render_template('form_lojista.html')


@app.route('/usuario/particular/confirmacao', methods=['GET'])
def confirm():
    return render_template('email_confirmacao.html')


@app.route('/admin/usuario/particular', methods=['GET'])
@motando_utils.ensure_logged_in
def admin_particular():
    global AUTH_COOKIE_NAME

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')
    
    auth_cookie = MotandoAuthCookie()    
    jwt_token = auth_cookie.get_jwt(cookie_value)

    usuario_particular = MotandoUsuarioParticular()    
    profile = usuario_particular.get_profile(jwt_token)

    if profile.get('status') == 'success':
        return render_template('admin_particular/home.html', profile=profile)
    else:
        return render_template('404.html')


@app.route('/admin/usuario/particular/anuncio', methods=['GET', 'POST'])
@motando_utils.ensure_logged_in
def form_anuncio():    
    global AUTH_COOKIE_NAME

    form = AnuncioForm()

    if request.method == 'POST':
        moto_marca_id = form.data.get('moto_marca')
        moto_modelo_id = form.data.get('moto_modelo')

        form.moto_marca.choices = [(moto_marca_id, moto_marca_id,)]
        form.moto_modelo.choices = [(moto_modelo_id, moto_modelo_id,)]

        if form.validate_on_submit():
            cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')    
                
            auth_cookie = MotandoAuthCookie()    
            jwt_token = auth_cookie.get_jwt(cookie_value)
            
            motando_anuncio = MotandoAnuncio()
            motando_anuncio.jwt_token = jwt_token

            resp = motando_anuncio.add(form.data)            

            if resp.get('status') == 'success':
                flask_flash(u'Novo anúncio cadastrado com sucesso.', 'success')

                return render_template('admin_particular/meus_anuncios.html')
                
            else: 
                flask_flash(u'Erro ao cadastrar novo anúncio.', 'error')
            
        else:
            flask_flash(u'Erro ao cadastrar novo anúncio. Por favor, corrigir os dados do formuládio.', 'error')

    return render_template('admin_particular/form_anuncio.html', form=form)


@app.route('/admin/usuario/particular/anuncio/imagem', methods=['POST', 'DELETE'])
@motando_utils.ensure_logged_in
@csrf.exempt
def anuncio_img_upload():    
    if request.method == 'POST':
        allowed_mimetype = ('image/jpeg', 'image/png', 'image/webp',)
        max_img_size = 5242880

        img = request.files.get('files[]')

        if img.mimetype in allowed_mimetype:
            img_data = img.read()
            img_data_bytes = len(img_data)

            if img_data_bytes > 0 and img_data_bytes <= max_img_size:
                cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')    
                
                auth_cookie = MotandoAuthCookie()    
                jwt_token = auth_cookie.get_jwt(cookie_value)
                
                motando_anuncio = MotandoAnuncio()
                motando_anuncio.jwt_token = jwt_token

                resp = motando_anuncio.add_img(filename=img.filename, data=img_data)

                if resp.get('status') == 'success':
                    return img.filename, resp.get('code')
                else:
                    return resp

    elif request.method == 'DELETE':
        filename = request.form.get('filename', '')

        if filename:
            return f'DELETED: {filename}', 200
    
    return 'Bad Request', 400


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400