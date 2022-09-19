#
# frontend/container-app/app/modules/motando_forms.py
#

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,  SubmitField, validators, ValidationError


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
