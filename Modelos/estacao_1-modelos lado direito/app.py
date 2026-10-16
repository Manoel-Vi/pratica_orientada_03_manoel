from flask import Flask, redirect, render_template, request, url_for
from sqlalchemy import select
from database import Base, engine
from models import Livro, Usuario

app = Flask(__name__)
Base.metadata.create_all(engine)

if __name__ == "__main__":
    app.run(debug=True)