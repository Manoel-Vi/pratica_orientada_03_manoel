from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine
from models import Livro, Usuario

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with Session(engine) as session:
        usuarios = session.scalars(select(Usuario)).all()
        livros = session.scalars(select(Livro)).all()
        return render_template('index.html', usuarios=usuarios, livros=livros)


@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = Usuario(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with Session(engine) as session:
            session.add(usuario)
            session.commit()
        return redirect(url_for('index'))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    with Session(engine) as session:
        usuarios = session.scalars(select(Usuario).order_by(Usuario.nome)).all()
        id_usuario = session.scalars(select(Usuario.id)).first()
        if request.method == 'POST':
            livro = Livro(
                titulo = request.form.get('titulo'),
                usuario_id = request.form.get(id_usuario)
            )
            session.add(livro)
            session.commit()
            return redirect(url_for('index'))
    return render_template('form_livro.html', usuarios=usuarios)

@app.route('/livros/listar', methods=['GET'])
def listar_livros():
    with Session(engine) as session:
        statement = select(Livro).order_by(Livro.titulo)
        livros = session.scalars(statement).all()

        return render_template('index.html', livros=livros)

@app.route('/usuarios/listar', methods=['GET'])
def listar_usuarios():
    with Session(engine) as session:
        statement = select(Usuario).order_by(Usuario.nome)
        usuarios = session.scalars(statement).all()

        return render_template('index.html', usuarios=usuarios)

@app.route('/logout')
def logout():
    return redirect(url_for('form_usuario'))
        
if __name__ == "__main__":
    app.run(debug=True)