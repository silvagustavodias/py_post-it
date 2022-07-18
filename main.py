from flask import Flask, render_template, url_for
from forms import FormLogin, FormCriarConta

app = Flask(__name__)
app.config['SECRET_KEY'] = '2c3e8d6ff5cc32e8a9d3b6b25ad4714f'


list_users = ['Gustavo', 'Débora', 'Pedro', 'Giselly']

# route caminho da homepage
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contatos')
def contato():
    return render_template('contato.html')

@app.route('/users')
def users():
    #Passando a variável para o código html
    return render_template('users.html', list_users=list_users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    return render_template('login.html', form_login = form_login, form_criarconta = form_criarconta)

if __name__ == '__main__':
    # valor para acatar mudanças automaticamente
    app.run(debug=True)
