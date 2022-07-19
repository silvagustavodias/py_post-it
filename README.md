
# Repositório de Notícias

Site para compartilhar notícias e opiniões e testar a utilização de Flask no back-end.

## Autores

- [@silvagustavodias](https://github.com/silvagustavodias)


## Stack utilizada

**Front-end:** BootStrap

**Back-end:** Flask

------
## Documentation
Para fins de estudos posteriores.

### main.py
#### imports realizados
* Flask: classe para inciar o app. importa-se Flask(__name__)
* render_template: para renderizar o html vindo da pasta template
* url_for: útil para tornar o endereço contido nos decorator uma variável
* request: para realizar requisições no site. Neste caso concreto foi utilizado para auxiliar na validação dos botões
* flash: mensagens de alertas do Flask
* redirect: método para redirecionar.

#### functions
As páginas são definidas por funções:

Ex:
@app.route('/contatos')
def contato():
    function....

A função def login() contém uma lógica de validação nos botões e no método já pronto de validação de formulário.


### models.py


### forms.py


### templates



