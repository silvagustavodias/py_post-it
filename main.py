from flask import Flask, render_template, url_for

app = Flask(__name__)


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

@app.route('/login')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    # valor para acatar mudanças automaticamente
    app.run(debug=True)
