#
# frontend/container-app/app/modules/motando_forms.py
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, validators, SelectField


class LoginForm(FlaskForm):
    email = StringField('Email', [
        validators.Email(message=(u'Endereço de e-mail está inválido.')),
        validators.DataRequired()        
    ], render_kw={'autofocus': True})

    senha = PasswordField('Senha', [
        validators.Length(min=10, max=50, message=u'A senha deve ter no mínimo 10 caracteres de comprimento.'),
        validators.DataRequired()
    ])

    submit = SubmitField(u'Enviar')

    def validate_email(self, field):
      pass


class CadastroUsuarioParticularForm(FlaskForm):
    brasil_estado = SelectField('Estado', [
        validators.DataRequired()
    ], coerce=int)

    brasil_cidade = SelectField('Cidade', [
        validators.DataRequired()
    ], coerce=int)

    nome = StringField('Nome', [
        validators.Length(min=10, max=500),
        validators.DataRequired()        
    ])

    email = StringField('Email', [
        validators.Email(message=(u'Endereço de e-mail está inválido.')),
        validators.DataRequired()        
    ])

    email_confirm = StringField('Confirme seu E-mail', [        
        validators.EqualTo('email', message='Os e-mails devem ser iguais.'),
        validators.DataRequired() 
    ])

    telefone = StringField('Telefone', [
        validators.Length(min=10, message='Telefone inválido.'),
        validators.DataRequired()        
    ])

    senha = PasswordField('Senha', [
        validators.Length(min=10, max=50, message=u'A senha deve ter no mínimo 10 caracteres de comprimento.'), 
        validators.DataRequired()
    ])

    senha_confirm = PasswordField('Confirme sua Senha', [
        validators.EqualTo('senha', message='As senhas devem ser iguais.'),        
        validators.DataRequired()
    ])

    submit = SubmitField(u'Enviar')
