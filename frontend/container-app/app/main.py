#
# frontend/container-app/app/main.py
#

import os
import json

from flask import Flask, flash as flask_flash, render_template
from flask import request, make_response, url_for, redirect, session, jsonify
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
               token = jwt['data']['access_token']

               auth_cookie = MotandoAuthCookie()

               auth_cookie.email = email
               auth_cookie.jwt_token = token
               
               cookie_value = auth_cookie.create()

               # TODO: implementar lógica para redirecionar 'admin_lojista'
               resp = make_response(redirect(url_for('admin_particular_home')))

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
@motando_utils.ensure_logged_in
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
def admin_particular_home():
    return render_template('admin_particular/home.html')    


@app.route('/admin/usuario/particular/conta', methods=['GET'])
@motando_utils.ensure_logged_in
def admin_particular_conta():
    global AUTH_COOKIE_NAME

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')
    
    auth_cookie = MotandoAuthCookie()    
    jwt_token = auth_cookie.get_jwt(cookie_value)

    usuario_particular = MotandoUsuarioParticular()    
    usuario_particular.jwt_token = jwt_token

    profile = usuario_particular.get_profile()

    if profile.get('status') == 'success':
        return render_template('admin_particular/minha_conta.html', profile=profile)
    else:
        return render_template('404.html')


@app.route('/admin/usuario/particular/anuncio', methods=['GET'])
@motando_utils.ensure_logged_in
def admin_particular_anuncio():
    """Painel dos Meus Anúncios.
    
    """
    return render_template('admin_particular/meus_anuncios.html')
   

@app.route('/admin/usuario/particular/anuncio/lista', methods=['GET'])
@motando_utils.ensure_logged_in
def admin_particular_anuncio_lista():
    """Lista os anúncios do usuário particular.
    
    """
    global AUTH_COOKIE_NAME

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')
    
    auth_cookie = MotandoAuthCookie()    
    jwt_token = auth_cookie.get_jwt(cookie_value)

    anuncio = MotandoAnuncio()    
    anuncio.jwt_token = jwt_token
    
    anuncio_list = anuncio.list()

    return jsonify(anuncio_list), anuncio_list.get('code')


@app.route('/admin/usuario/particular/anuncio/novo', methods=['GET', 'POST'])
@motando_utils.ensure_logged_in
def novo_anuncio():    
    """Formulário para cadastro de um Novo Anúncio.
    
    """
    global AUTH_COOKIE_NAME

    form = AnuncioForm()

    if request.method == 'POST':
        moto_marca_id = form.data.get('moto_marca')
        moto_modelo_id = form.data.get('moto_modelo')

        form.moto_marca.choices = [(moto_marca_id, moto_marca_id,)]
        form.moto_modelo.choices = [(moto_modelo_id, moto_modelo_id,)]

        img_lista = form.data.get('img_lista', '')

        # valida o formulário e se há imagens junto ao anúncio.
        if form.validate_on_submit() and img_lista:
            cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')    
                
            auth_cookie = MotandoAuthCookie()    
            jwt_token = auth_cookie.get_jwt(cookie_value)
            
            anuncio = MotandoAnuncio()
            anuncio.jwt_token = jwt_token

            resp = anuncio.add(data=form.data)            

            if resp.get('status') == 'success':
                flask_flash(u'Novo anúncio cadastrado com sucesso.', 'success')

                return redirect(url_for('admin_particular_anuncio')) 
            else: 
                flask_flash(u'Erro ao cadastrar novo anúncio.', 'error')
            
        else:
            flask_flash(u'Erro ao cadastrar novo anúncio. Por favor, corrigir os dados do formuládio.', 'error')

    return render_template('admin_particular/form_anuncio.html', form=form)


@app.route('/admin/usuario/particular/anuncio/<int:anuncio_id>', methods=['GET', 'POST'])
@motando_utils.ensure_logged_in
def edit_anuncio(anuncio_id: int):
    """Edita um anúncio em particular.
    
    """
    global AUTH_COOKIE_NAME

    cookie_value = request.cookies.get(AUTH_COOKIE_NAME, '')
    
    auth_cookie = MotandoAuthCookie()    
    jwt_token = auth_cookie.get_jwt(cookie_value)

    anuncio = MotandoAnuncio()
    anuncio.jwt_token = jwt_token

    # Obtém JSON do anúncio.
    resp = anuncio.get(anuncio_id)   

    if resp.get('status') != 'success':
        return render_template('404.html'), 404

    # Converte o JSON para um dicionário Python.
    anuncio_data = json.loads(resp.get('data'))

    moto_marca = anuncio_data.get('moto_marca')
    moto_modelo = anuncio_data.get('moto_modelo')

    form = AnuncioForm(data=anuncio_data)
    
    if request.method == 'POST':
        moto_marca_id = form.data.get('moto_marca')
        moto_modelo_id = form.data.get('moto_modelo')

        form.moto_marca.choices = [(moto_marca_id, moto_marca_id,)]
        form.moto_modelo.choices = [(moto_modelo_id, moto_modelo_id,)]

        img_lista = form.data.get('img_lista', '')

        # valida o formulário e se há imagens junto ao anúncio.
        if form.validate_on_submit() and img_lista:
            resp = anuncio.update(anuncio_id=anuncio_id, data=form.data)     

            if resp.get('status') == 'success':
                flask_flash(u'Anúncio atualizado com sucesso. Aguarde a sua republicação...', 'success')

                return redirect(url_for('admin_particular_anuncio')) 
            else: 
                flask_flash(u'Erro ao atualizar anúncio.', 'error')
            
        else:            
            flask_flash(u'Erro ao atualizar anúncio. Por favor, corrigir os dados do formuládio.', 'error')                   

    return render_template('admin_particular/form_anuncio.html', anuncio_id=anuncio_id, 
        form=form, moto_marca=moto_marca, moto_modelo=moto_modelo)            


@app.route('/admin/usuario/particular/novo/anuncio/imagem', methods=['POST', 'DELETE'])
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
                
                anuncio = MotandoAnuncio()
                anuncio.jwt_token = jwt_token

                resp = anuncio.add_img(filename=img.filename, data=img_data)

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