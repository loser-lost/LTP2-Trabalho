from database import connect
import database

class Livro:

  def __init__(self, id_livro, nome_livro, autor_livro, resumo_livro):
    self._livro = id_livro
    self.nome_livro = nome_livro
    self.autor_livro = autor_livro
    self.resumo_livro = resumo_livro

  #Ver

    
  #criar  
  @staticmethod
  def cadLivro(nome_livro, autor_livro, resumo_livro):

    connection = database.connect()

    sql = "INSERT INTO livros (nome_livro, autor_livro, resumo_livro) VALUES (?, ?, ?)"
    values = (nome_livro, autor_livro, resumo_livro)
    
    cursor = connection.cursor()
    cursor.execute(sql, values)
    
    connection.commit()
    connection.close()

    return Livro(cursor.lastrowid, nome_livro, autor_livro, resumo_livro)
  
  @staticmethod
  def getLivroByID(id_livro):
      connection = database.connect()
      cursor = connection.cursor()
  
      sql = "SELECT * FROM livros WHERE id_livro = ?"
      cursor.execute(sql, (id_livro,))
      livro_data = cursor.fetchone()
  
      cursor.close()
      connection.close()
  
      if livro_data:
          return Livro(*livro_data)
      else:
          return None
  
  
  #editar
  
  @staticmethod
  def editLivro(id_livro, nome_livro, autor_livro, resumo_livro):
  
      connection = database.connect()
      if not Livro.getLivroByID(id_livro):
          raise Exception("Livro com ID {} não encontrado.".format(id_livro))
  
      
      sql = "UPDATE livros SET nome_livro=?, autor_livro=?, resumo_livro=? WHERE id_livro=?"
      values = ( nome_livro, autor_livro, resumo_livro, id_livro)
  
      cursor = connection.cursor()
      print("sql:", sql)
      print("Values", values)
      cursor.execute(sql, values)
  
      
      connection.commit()
      cursor.close()
      connection.close()
      return Livro(id_livro, nome_livro, autor_livro, resumo_livro)
