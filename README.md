
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

__descrição__: classe para iniciar o APP, a Database e a Bcrypt. Importante chamar a importação das 'routes' ao fim da classe para que os endereços dos sites estejam iniciados.

#### imports realizados
* Flask: biblioteca para construção de sites em python
* SQLAlchemy: biblioteca para utilização de banco de dados
* Bcrypt: módulo para criptografar a senha na hora do login
* routes: importar ao fim do módulo.

## models.py

__descrição__: módulo  vão formar as tabelas dos banco de dados a partir de classes.
Aqui também são tratados os relacionamentos entre as classes.

#### imports realizados
*  database importada da classe __init__
* datetime para executar uma função para data do Post

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
  
    

## forms.py
#### imports
* Flask: classe para inciar o app. importa-se Flask(__name__)
* render_template: para renderizar o html vindo da pasta template
* url_for: útil para tornar o endereço contido nos decorator uma variável
* request: para realizar requisições no site. Neste caso concreto foi utilizado para auxiliar na validação dos botões
* flash: mensagens de alertas do Flask
* redirect: método para redirecionar.

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