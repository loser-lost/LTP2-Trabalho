from database import connect
import database


#from connect import connection
class User:

  def __init__(self, id, nome, email, senha):
    self.id = id
    self.nome = nome
    self.email = email
    self.senha = senha

  @staticmethod
  def login(email, senha):
    # Conectar ao banco de dados
    connection = database.connect()
  
    # Preparar a consulta SQL
    sql = "SELECT * FROM usuarios WHERE email = ? AND senha = ?"
    values = (email, senha)
  
    # Executar a consulta SQL
    cursor = connection.cursor()
    cursor.execute(sql, values)
    result = cursor.fetchone()
    connection.close()
    print(result)

    if result is not None:
      id, nome, email, senha = result
      user = User(id, nome, email, senha)
      return user
    else:
      raise ValueError("Credenciais de login inválidas.")
    
  @staticmethod
  def cadUser(nome, email, senha):

    connection = database.connect()

    sql = "INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)"
    values = (nome, email, senha)

    cursor = connection.cursor()
    cursor.execute(sql, values)

    connection.commit()
    connection.close()

    return User(cursor.lastrowid, nome, email, senha)

  