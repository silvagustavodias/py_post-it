from flask import render_template, redirect, url_for, flash, request
from post_it import app, database, bcrypt
from post_it.forms import FormLogin, FormCriarConta
from post_it.models import Usuario


list_users = ['Gustavo','André','Débora','Carol','Pedro',]

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

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        flash(f'Login feito com suceso no e-mail: {form_login.email.data}', 'alert-success')
        return redirect(url_for('home'))

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        #Criptografando senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        #Criando Usuário
        new_user = Usuario(username= form_criarconta.username.data,
                           email= form_criarconta.email.data,
                           senha= senha_cript)
        # Add  a sessão
        database.session.add(new_user)
        # Commit na sessão
        database.session.commit()
        flash(f'Conta criada usuário: {form_criarconta.email.data}', 'alert-success')
        return redirect(url_for('home'))

    return render_template('login.html', form_login = form_login, form_criarconta = form_criarconta)
