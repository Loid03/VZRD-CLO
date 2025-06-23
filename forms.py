from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, TextAreaField, BooleanField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, NumberRange
from VzrdClothing.models_db import User

class LoginForm(FlaskForm):
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar de mim')

class RegisterForm(FlaskForm):
    username = StringField('Nome de usuário', validators=[
        DataRequired(), 
        Length(min=3, max=20, message='Nome de usuário deve ter entre 3 e 20 caracteres')
    ])
    email = EmailField('E-mail', validators=[DataRequired(), Email()])
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Telefone', validators=[Length(max=20)])
    password = PasswordField('Senha', validators=[
        DataRequired(), 
        Length(min=6, message='Senha deve ter pelo menos 6 caracteres')
    ])
    password_confirm = PasswordField('Confirmar Senha', validators=[
        DataRequired(), 
        EqualTo('password', message='Senhas não coincidem')
    ])
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nome de usuário já existe. Escolha outro.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('E-mail já cadastrado. Faça login ou use outro e-mail.')

class ProfileForm(FlaskForm):
    first_name = StringField('Nome', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Sobrenome', validators=[DataRequired(), Length(max=50)])
    phone = StringField('Telefone', validators=[Length(max=20)])
    address = TextAreaField('Endereço')
    city = StringField('Cidade', validators=[Length(max=100)])
    state = StringField('Estado', validators=[Length(max=50)])
    zipcode = StringField('CEP', validators=[Length(max=10)])

class ProductForm(FlaskForm):
    name = StringField('Nome do Produto', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Descrição', validators=[DataRequired()])
    price = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0.01)])
    image_url = StringField('URL da Imagem', validators=[DataRequired(), Length(max=500)])
    category = SelectField('Categoria', choices=[
        ('oversized', 'Oversized'),
        ('streetwear', 'Streetwear'),
        ('casual', 'Casual'),
        ('premium', 'Premium')
    ], default='oversized')
    size_options = StringField('Tamanhos Disponíveis', validators=[Length(max=100)], default='P,M,G,GG,XG')
    stock_quantity = IntegerField('Quantidade em Estoque', validators=[NumberRange(min=0)], default=50)
    featured = BooleanField('Produto em Destaque')
    in_stock = BooleanField('Em Estoque', default=True)

class OrderStatusForm(FlaskForm):
    status = SelectField('Status do Pedido', choices=[
        ('pending', 'Pendente'),
        ('confirmed', 'Confirmado'),
        ('shipped', 'Enviado'),
        ('delivered', 'Entregue'),
        ('cancelled', 'Cancelado')
    ])
    tracking_number = StringField('Número de Rastreamento', validators=[Length(max=100)])
    admin_notes = TextAreaField('Observações do Admin')

class SearchForm(FlaskForm):
    query = StringField('Buscar produtos...', validators=[Length(max=100)])
    category = SelectField('Categoria', choices=[
        ('', 'Todas as categorias'),
        ('oversized', 'Oversized'),
        ('streetwear', 'Streetwear'),
        ('casual', 'Casual'),
        ('premium', 'Premium')
    ])
    min_price = DecimalField('Preço mínimo', validators=[NumberRange(min=0)])
    max_price = DecimalField('Preço máximo', validators=[NumberRange(min=0)])