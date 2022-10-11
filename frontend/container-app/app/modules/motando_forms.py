#
# frontend/container-app/app/modules/motando_forms.py
#

from flask_wtf import FlaskForm
from wtforms import validators
from wtforms import StringField, SelectField, IntegerField, BooleanField, HiddenField
from wtforms import PasswordField, DecimalField, TextAreaField, SubmitField


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


class AnuncioForm(FlaskForm):
    cor_choices = [
        ('Não especificado', 'Selecione a Cor',), 
        ('azul', 'Azul',), ('verde', 'Verde',), ('vermelho', 'Vermelho',),
        ('preto', 'Preto',), ('laranja', 'Laranja',), ('amarelo', 'Amarelo',),
        ('roxo', 'Roxo',), ('branco', 'Branco',), ('marrom', 'Marrom',), 
        ('prata', 'Prata',), ('outro', 'Outro',),
    ]

    freios_choices = [
        ('Não especificado', 'Selecione os Freios',), 
        ('disco', 'Disco',), ('combinado', 'Combinado',), ('abs', 'ABS',),
        ('tambor', 'Tambor',), 
    ]

    partida_choices = [
        ('Não especificado', 'Selecione o Tipo da Partida',),
        ('pedal', 'Pedal',), ('eletrica', 'Elétrica',), ('ambos', 'Ambos',),
        ('outro', 'Outro',),
    ]

    refrigeracao_choices = [
        ('Não especificado', 'Selecione o Tipo de Refrigeração',),
        ('liquida', 'Líquida',), ('ar', 'Ar',),
    ]

    estilo_choices = [
        ('Não especificado', 'Selecione o Estilo da Motocicleta',),
        ('naked', 'Naked',), ('sport', 'Sport',), ('bigtrail', 'Big Trail',),
        ('caferacer', 'Café Racer',), ('custom', 'Custom',), ('classica', 'Clássica',),
        ('eletrica', 'Elétrica',), ('minimoto', 'Minimoto',), ('offroad', 'Off-Road',),
        ('scooter', 'Scooter',), ('street', 'Street',), ('supermotard', 'SuperMotard',),
        ('triciclo', 'Triciclo',), ('touring', 'Touring',), ('quadriciclo', 'Quadriciclo',),
        ('scrambler', 'Scrambler',), ('ciclomotor', 'Ciclomotor',), ('cub', 'Cub',),
        ('outro', 'Outro',),
    ]

    origem_choices = [
        ('Não especificado', 'Selecione a Origem da Motocicleta',),
        ('nacional', 'Nacional',), ('importada', 'Importada',),
    ]

    moto_marca = SelectField('Marca', [
        validators.DataRequired()
    ], coerce=int)

    moto_modelo = SelectField('Modelo', [
        validators.DataRequired()
    ], coerce=int)

    ano_fabricacao = StringField('Ano de Fabricação', [
        validators.Length(min=4, max=4, message='Ano/Fabricação inválido.'),
        validators.DataRequired()        
    ])

    ano_modelo = StringField('Ano do Modelo', [
        validators.Length(min=4, max=4, message='Ano/Modelo inválido.'),
        validators.DataRequired()        
    ])

    placa = StringField('Placa', [
        validators.Length(min=4, max=10, message='Número de Placa inválido.'),
        validators.DataRequired()        
    ])

    km = IntegerField('KM', [        
        validators.optional()
    ])

    zero_km = BooleanField('Zero KM', [
        validators.optional()
    ], default=False)

    cor = SelectField('Cor Predominante', [
        validators.DataRequired(message='É necessário informa uma Cor.')
    ], choices=cor_choices, default='Não especificado')

    #preco = DecimalField('Preço', [
    #    validators.DataRequired(),
    #    validators.NumberRange(min=1, message=u'Preço inválido.'),
    #], places=8)
    preco = StringField('Preço', [
        validators.DataRequired()
    ], default='0.00')

    frase_vendedora = StringField('Frase Vendedora', [  
        validators.length(max=500),
        validators.optional()
    ])

    descricao = TextAreaField('Descrição do Anúncio', [
        validators.length(max=2000),
        validators.optional()
    ])

    opcional_alarme = BooleanField('Alarme', [
        validators.optional()
    ], default=False)

    opcional_bau = BooleanField('Baú / Malas', [
        validators.optional()
    ], default=False)

    opcional_computador = BooleanField('Computador de Bordo', [
        validators.optional()
    ], default=False)

    opcional_gps = BooleanField('GPS', [
        validators.optional()
    ], default=False)

    aceita_contraoferta = BooleanField('Aceita contra oferta', [
        validators.optional()
    ], default=False)

    aceita_troca = BooleanField('Aceita troca', [
        validators.optional()
    ], default=False)

    doc_ok = BooleanField('Documentação em dia', [
        validators.optional()
    ], default=False)

    sinistro = BooleanField('Possui Sinistro', [
        validators.optional()
    ], default=False)

    trilha_pista = BooleanField('Moto preparada para trilha ou pista', [
        validators.optional()
    ], default=False)

    freios = SelectField('Freios', [
        validators.optional()
    ], choices=freios_choices, default='Não especificado')

    tipo_partida = SelectField('Tipo de partida', [
        validators.optional()
    ], choices=partida_choices, default='Não especificado')

    refrigeracao = SelectField('Refrigeração do Motor', [
        validators.optional()
    ], choices=refrigeracao_choices, default='Não especificado')

    estilo = SelectField('Estilo', [
        validators.optional()
    ], choices=estilo_choices, default='Não especificado')

    origem = SelectField('Origem', [
        validators.optional()
    ], choices=origem_choices, default='Não especificado')

    img_lista = HiddenField([
        validators.DataRequired()
    ])

    # TODO: validações zero_km, km, ano_fabricacao <= ano_modelo.
    
    submit = SubmitField(u'Concluír Anúncio')