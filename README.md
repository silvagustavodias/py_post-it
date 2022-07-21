
# Repositório de Notícias

Site para compartilhar notícias e opiniões e testar a utilização de Flask no back-end.

## Autores

- [@silvagustavodias](https://github.com/silvagustavodias)


## Stack utilizada

**Front-end:** BootStrap

**Back-end:** Flask

------
# Documentation
Para fins de estudos posteriores. Documentação construída em forma de relato para construção de estudos.

## main.py
#### imports realizados
* O App contido na função __init__.py

Main roda exclusivamente o app.

## __init__py

__descrição__: classe para instanciar as classes mais gerais: APP, a Database, a Bcrypt e o LoginManager. Importante chamar a importação das 'routes' ao fim da classe para que os endereços dos sites estejam iniciados.

#### imports realizados
* Flask: biblioteca para construção de sites em python
* SQLAlchemy: biblioteca para utilização de banco de dados
* Bcrypt: módulo para criptografar a senha na hora do login
* LoginManager: Módulo do Flask para tratar o login. Necessário passar algumas configurações:
  * login_view = função (route) que realiza o login.
  * login_message = mensagem exibida após o login
  * login_message_category = passar a classe do BootStrap do alerta da mensagem exibida
* routes: importar ao fim do módulo.

## models.py

__descrição__: módulo  que vai formar as tabelas dos banco de dados a partir de classes.
Aqui também são tratados os relacionamentos entre as classes.

#### imports realizados
* database importada da classe __init__
* datetime para executar uma função para data do Post
* flask_login - UserMixin: import para tratar o usuário logado. Passar a classe UserMixin como parâmetro de init da classe User
#### Classes
_Passar sempre o database.Model como parâmetro da classe. [Extensão da classe]._

**colunas**: database.Column(_destacar o tipo do dado_ EX: database.String)
_parâmetros úteis: nullable=False - não nulo; default = 'valor padrão'; unique=True [valor único]_

**relacionamentos**: database.relationship(_informar a classe_, _backref_ comando para realizar o link com a outra classe.)

**ForeignKey**: passada pelo database.ForeignKey('usuario.id') 

* Usuário:
  * id: primary_key = True
  * username:
  * senha:
  * email:
  * foto_perfil:
  * posts: database.relationship
  * interesses:

* Post:
  * id: primary_key = True
  * titulo:
  * corpo:
  * data_criacao:
  * id_usuario: foreign_key

####  Functions
* def load_user(id_usuario): Função para pegar o usuário. passar o decorator @login_manager.user_loader, para certificar que esta função é a responsável por encontrar o usuário logado.
    

## forms.py

__descrição__: módulo de classes que representam os formulários do site. Para criar um formulário com o Framework FLASK basta criar uma classe e instanciar um FLASKFORM como parâmetro dessa classe.
#### imports
* Flask: classe para inciar o app. importa-se Flask(__name__)
* render_template: para renderizar o html vindo da pasta template
* url_for: útil para tornar o endereço contido nos decorator uma variável
* request: para realizar requisições no site. Neste caso concreto foi utilizado para auxiliar na validação dos botões
* flash: mensagens de alertas do Flask
* redirect: método para redirecionar.

#### Classes

Para cada variável do FlaskForm deve ser declarado o tipo de campo e seus validadores.
Cada campo é instanciado com seu "label" e uma lista de validadores: EX: StringField("Nome: ", validators=[Length(4,20), DataRequired()])
Principais campos utilizados:
1. StringField - campo de String. Validadores: DataRequired(), Email(), Length(6,20)
2. PasswordField - campo para senhas. validators = DataRequired()
3. SubmitField - para botões de submit form
4. BooleanField - Devolve True ou False
5. FileField - Para campos de upload. validators = FileAllowed([passar uma lista com as extensões possíveis])

##### FormCriarConta(FlaskForm)

* username - StringField
* email - StringField
* senha - PasswordField
* confirmacao_senha - PasswordField
* botao_submit_criarconta - SubmitField


##### FormLogin(FlaskForm)

* email = StringField
* senha = PasswordField
* lembrar_dados = BooleanField
* botao_submit_login = SubmitField

##### FormEditarPerfil(FlaskForm)
* username = StringField
* email = StringField
* foto_perfil = FileField
* botao_submit_editarperfil = SubmitField

#### functions
* validate_email(self, email):
  _descrição_: _para conferir se existe mais algum e-mail cadastrado. Utilizada a partir do login._




## routes.py
#### imports


#### functions
As páginas são definidas por funções:

Ex:
@app.route('/contatos')
def contato():
function....

A função def login() contém uma lógica de validação nos botões e no método já pronto de validação de formulário.

## templates
### base.html

### contato.html


### home.html

### login.html


### navbar.html


### users.html