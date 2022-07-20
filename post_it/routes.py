from flask import render_template, redirect, url_for, flash, request
from post_it import app, database, bcrypt
from post_it.forms import FormLogin, FormCriarConta, FormEditarPerfil
from post_it.models import Usuario
from flask_login import login_user, logout_user, current_user, login_required


list_users = ['Gustavo','André','Débora','Carol','Pedro',]

# route caminho da homepage
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/contatos')
def contato():
    return render_template('contato.html')

@app.route('/users')
@login_required
def users():
    #Passando a variável para o código html
    return render_template('users.html', list_users=list_users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com suceso no e-mail: {form_login.email.data}', 'alert-success m-2')
            #pegar o parâmetro NEXT para redirecionar para onde o usuário estava tentando entrar
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger m-2')

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

        usuario = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        login_user(usuario)
        flash(f'Conta criada usuário: {form_criarconta.email.data}', 'alert-success m-2')
        return redirect(url_for('home'))

    return render_template('login.html', form_login = form_login, form_criarconta = form_criarconta)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso', 'alert-success m-2')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil = foto_perfil)

@app.route('/post/criar')
@login_required
def criar_post():
    return render_template('criar_post.html')

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)