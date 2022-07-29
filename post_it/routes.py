from flask import render_template, redirect, url_for, flash, request, abort
from post_it import app, database, bcrypt
from post_it.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, FormRespostaPost
from post_it.models import Usuario, Post, Resposta
from flask_login import login_user, logout_user, current_user, login_required
import secrets
from PIL import Image
import os


# route caminho da homepage
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc())
    return render_template('home.html', posts=posts)


@app.route('/contatos')
def contato():
    return render_template('contato.html')


@app.route('/users')
@login_required
def users():
    list_users = Usuario.query.all()
    # Passando a variável para o código html
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
            # pegar o parâmetro NEXT para redirecionar para onde o usuário estava tentando entrar
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            return redirect(url_for('home'))
        else:
            flash(f'Falha no login. E-mail ou senha incorretos.', 'alert-danger m-2')

    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        # Criptografando senha
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)

        # Criando Usuário
        new_user = Usuario(username=form_criarconta.username.data,
                           email=form_criarconta.email.data,
                           senha=senha_cript)
        # Add  a sessão
        database.session.add(new_user)
        # Commit na sessão
        database.session.commit()

        usuario = Usuario.query.filter_by(email=form_criarconta.email.data).first()
        login_user(usuario)
        flash(f'Conta criada usuário: {form_criarconta.email.data}', 'alert-success m-2')
        return redirect(url_for('home'))

    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


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
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        new_post = Post(titulo=form.titulo.data, corpo=form.corpo.data, author=current_user)
        database.session.add(new_post)
        database.session.commit()
        flash('Post criado com sucesso', 'alert-success mt-2 mb-2')
        return redirect(url_for('home'))
    return render_template('criar_post.html', form=form)


def salvar_imagem(imagem):
    # add o código-único no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    image_path = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # Reduzir imagem
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar imagem
    imagem_reduzida.save(image_path)
    return nome_arquivo


def atualizar_interesses(form):
    lista_interesses_aux = []
    for campo in form:
        if 'interesse_' in campo.name:
            if campo.data:
                lista_interesses_aux.append(campo.label.text)
    if len(lista_interesses_aux) == 0:
        return

    return ';'.join(lista_interesses_aux)


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            # Adicionando código aleatório na imagem
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem

            # mudar o campo foto perfil do current user
        current_user.interesses = atualizar_interesses(form)
        database.session.commit()
        flash('Perfil atualizado com sucesso', 'alert-success')
        return redirect(url_for('perfil'))

    # Se o formulário não tiver enviando nadad (método POST), ele já preenche automático.
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        for campo in form:
            if 'interesse_' in campo.name:
                if campo.label.text in current_user.interesses:
                    campo.data = True

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@login_required
@app.route('/post/<post_id>/editar', methods=['GET', 'POST'])
def editar_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash("Post atualizado com sucesso", "alert-success mt-2")
            return redirect(url_for('exibir_post', post_id=post.id))
        else:
            flash("Você não tem acesso para editar post de outro usuário", "alert-danger")
            redirect('home')
    return render_template('editarpost.html', form=form, post=post)


# Controle de páginas de post. Cada post uma página. Passa a url para a função ID
@login_required
@app.route('/post/<post_id>', methods=['GET', 'POST'])
def exibir_post(post_id):
    post = Post.query.get(post_id)
    comentarios = Resposta.query.filter_by(id_post=post_id)
    if current_user == post.author:
        form = True
    else:
        form = None
    return render_template('post.html', comentarios=comentarios, post=post, form=form)


@login_required
@app.route('/post/comentario/<post_id>', methods=['GET', 'POST'])
def resposta_post(post_id):
    post = Post.query.get(post_id)
    form = FormRespostaPost()
    if form.validate_on_submit():
        new_coment = Resposta(comentario=form.comentario.data, post=post)
        database.session.add(new_coment)
        database.session.commit()
        flash('Post respondido com sucesso', 'alert-success mt-2 mb-2')
        return redirect(url_for('home'))

    return render_template('resposta.html', form=form)

@login_required
@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.author:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluído com sucesso.', 'alert-danger mt-2 mb-2')
        return redirect(url_for('home'))
    else:
        abort(403)





