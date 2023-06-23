from flask import Flask
from flask import render_template, request, session, redirect, url_for, flash
from User import User
from Livro import Livro
import database
#from User import loginUsuario

app = Flask(__name__)
app.secret_key = 'chavesecreta'  # Define uma chave secreta para uso na sessão

@app.route('/')
def index():
    connection = database.connect()
    
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM livros")
    
    result = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return render_template('home.html',result=result)
  
@app.route('/cadastro')
def cad_rote():
    return render_template('cadastro.html')

@app.route('/login')
def log_rote():
  #  if 'user_id' in session:
      # Usuário já está logado, redirecionar para outra página
   #   return redirect(url_for('index'))
    #else:
      # Usuário não está logado, renderizar o template de login
      return render_template('login.html')

@app.route('/pgCadlivro')
def pgcadlivro():
  return render_template('cadlivro.html') 
  
@app.route('/edit/<int:id>')
def edit(id):
    connection = database.connect()

    # ID do livro a ser selecionado
    livro_id = id
    print (livro_id)
    cursor = connection.cursor()
    # Executar consulta
    cursor.execute("SELECT id_livro, nome_livro, autor_livro, resumo_livro FROM livros WHERE id_livro = ?", (livro_id,))    
    
    resultado = cursor.fetchone()

    print (resultado)
    cursor.close()
    connection.close()
    return render_template('edit.html',resultado=resultado)

@app.route('/editar_livro', methods=['POST'])
def editar_livro():
    livro_id = request.form['livro_id']
    # Lógica para obter o livro com o ID fornecido do banco de dados
    livro = Livro.getLivroByID(livro_id)
    if livro:
        # Redirecionar para a página de edição com o ID do livro obtido
        print (livro_id)
        return redirect(url_for('edit', id=livro_id))
    else:
        return "Livro não encontrado"
#-------------------------------ROTAS DE Login--------------------------------------------------------------#
@app.route('/delete_livro', methods=['DELETE','POST'])

def delete_livro():
    livro_id = request.form['livro_id']
    # Lógica para obter o livro com o ID fornecido do banco de dados
    livro = Livro.getLivroByID(livro_id)
    if livro:
      # Excluir o livro do banco de dados
      connection = database.connect()
      cursor = connection.cursor()
      cursor.execute("DELETE FROM livros WHERE id_livro = ?;", (livro_id,))
      connection.commit()
      cursor.close()
      connection.close()

      # Redirecionar para a página inicial com uma mensagem de sucesso
      flash('Livro excluído com sucesso', 'success')
      return redirect(url_for('index'))
        
    else:
        return "Livro não encontrado"
      #-------------------------------delete--------------------------------------------------------------#

@app.route('/entrar', methods=['POST'])
def login():
    try:
        if request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
          
            # Passa as informações de login para o controlador
            user = User.login(email, senha)
                
            if user is not None:
                session['user_id'] = user.id  # Armazena o ID do usuário na sessão
                return redirect(url_for('index'))  # Redireciona para a página inicial após o login
            else:
                return render_template('login.html')

    except Exception as e:
        raise Exception("Ocorreu um erro ao autenticar o usuário: {}".format(str(e)))


@app.route('/logout', methods=['GET'])
def logout():
    # Remove o usuário da sessão, se estiver presente
    session.clear()
    return redirect(url_for('log_rote'))
#---------------------------------------------------------------------------------------------

@app.route('/cadastrar', methods=['GET','POST'])
def cadastro():
    try:
      nome = request.form['nome']
      email = request.form['email']
      senha = request.form['senha']
  
      resultado = User.cadUser(nome, email, senha)
  
      if resultado:
        return render_template('home.html')
      else:
        return "Erro"
    except Exception as e:
        raise Exception("Ocorreu um erro ao criar o usuário: {}".format(str(e)))




#-------------------------------ROTAS DE Livros--------------------------------------------------------------#

@app.route('/cadastrar_livro', methods=['GET','POST'])
def cadastrar_livro():
    try:
      nome_livro = request.form['nome_livro']
      autor_livro = request.form['autor_livro']
      resumo_livro = request.form['resumo_livro']
  
      resultado = Livro.cadLivro(nome_livro, autor_livro, resumo_livro)
  
      if resultado:
        return redirect(url_for('index'))
      else:
        return "Erro"
    except Exception as e:
        raise Exception("Ocorreu um erro ao criar um livro: {}".format(str(e)))

@app.route('/salvar_edicao', methods=['POST'])
def salvar_edicao():
    try:
        id_livro = request.form['id_livro']
        nome_livro = request.form['nome_livro']
        autor_livro = request.form['autor_livro']
        resumo_livro = request.form['resumo_livro']
        
        # Realize a lógica para salvar as alterações no livro com o ID fornecido
        executar = Livro.editLivro(id_livro, nome_livro, autor_livro, resumo_livro)
        if executar:
          return redirect(url_for('index'))  # Redireciona para a página de listagem de livros após salvar as alterações
        else:
            raise Exception("Livro não encontrado")

    except Exception as e:
        raise Exception("Ocorreu um erro ao salvar a edição do livro: {}".format(str(e)))



app.run(host='0.0.0.0', port=81)