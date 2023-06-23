import sqlite3
from replit import db

def connect():
  conn = sqlite3.connect('myDatabase.db')
  conn.execute("CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT, email TEXT, senha TEXT);")
  conn.execute("CREATE TABLE IF NOT EXISTS livros (id_livro INTEGER PRIMARY KEY, nome_livro TEXT, autor_livro TEXT, resumo_livro TEXT);")
  return conn

