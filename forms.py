from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, SelectField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from models import User
from extensions import db

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Senha', 
                                  validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Registrar')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este email já está em uso. Escolha outro.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar = BooleanField('Lembrar de mim')
    submit = SubmitField('Entrar')

class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar')

class PasswordResetForm(FlaskForm):
    senha = PasswordField('Nova Senha', validators=[DataRequired(), Length(min=6)])
    confirmar_senha = PasswordField('Confirmar Nova Senha', 
                                  validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Redefinir Senha')

class ProjectForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')])
    tags = StringField('Tags (separadas por vírgula)', validators=[Length(max=200)])
    status = SelectField('Status', choices=[('draft', 'Rascunho'), ('published', 'Publicado')])
    submit = SubmitField('Salvar')

class AchievementForm(FlaskForm):
    titulo = StringField('Título', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    data_conquista = StringField('Data', validators=[DataRequired()])
    imagem = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Apenas imagens!')])
    submit = SubmitField('Salvar')

class CommentForm(FlaskForm):
    conteudo = TextAreaField('Comentário', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Comentar')