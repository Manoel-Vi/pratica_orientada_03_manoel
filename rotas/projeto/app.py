from flask import Flask, render_template, request, url_for, redirect
from sqlalchemy import select

from database import Base, SessionLocal, engine
from models import Book, User

app = Flask(__name__)
Base.metadata.create_all(engine)


@app.route('/')
def index():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User.nome)).all()
        livros = session.scalars(select(Book.titulo)).all()
    return render_template('index.html', usuarios=usuarios, livros=livros)


@app.route('/usuario/novo', methods=['POST', 'GET'])
def form_usuario():
    if request.method == 'POST':
        usuario = User(
            nome=request.form.get('nome'),
            email=request.form.get('email')
        )
        with SessionLocal() as session:
            session.add(usuario)
            session.commit()
        return redirect(url_for('index'))
    return render_template('form_usuario.html')


@app.route('/livros/novo', methods=['GET', 'POST'])
def form_livro():
    with SessionLocal() as session:
        usuarios = session.scalars(select(User).order_by(User.nome)).all()
        if request.method == 'POST':
            livro = Book(
                titulo=request.form.get('titulo'),
                usuario_id=int(request.form.get('usuario_id'))
            )
            session.add(livro)
            session.commit()
            return redirect(url_for('index'))
    return render_template('form_livro.html', usuarios=usuarios)

@app.route('/livros/listar', methods=['GET'])
def listar_livros():
    with SessionLocal() as session:
        statement = select(Book).order_by(Book.titulo)
        livros = session.scalars(statement).all()

        return render_template('index.html', livros=livros)

@app.route('/usuarios/listar', methods=['GET'])
def listar_usuarios():
    with SessionLocal() as session:
        statement = select(User).order_by(User.nome)
        usuarios = session.scalars(statement).all()

        return render_template('index.html', usuarios=usuarios)
        
if __name__ == "__main__":
    app.run(debug=True)