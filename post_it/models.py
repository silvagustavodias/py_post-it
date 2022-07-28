from post_it import database, login_manager
from flask_login import UserMixin
from datetime import datetime

#Função para encontrar o usuário. Utiliza-se o método query.get pois temos a primary_key do Db.
# Passa o decorator do login_manager para certificar que esta função encontra os usuários.
@login_manager.user_loader
def load_user(id_usuario):
    usuario = Usuario.query.get(int(id_usuario))
    return usuario


#Utiliza-se o UserMixin para passar que essa classe é a classe responsável pelos Login.
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    senha = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    foto_perfil = database.Column(database.String, default='default.png')
    posts = database.relationship('Post', backref='author', lazy=True)
    interesses = database.Column(database.String, nullable=False, default='Não informado')


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    resposta = database.relationship('Resposta', backref='post', lazy=True)


class Resposta(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    comentario = database.Column(database.Text, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_post = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)