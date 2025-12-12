import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'senha_hugo_wendell' 


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_trabalho3B'
}

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auditoria')
def listar_auditoria():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Auditoria_Logs ORDER BY Data_hora DESC LIMIT 50")
    logs = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('auditoria_lista.html', logs=logs)

@app.route('/autores')
def listar_autores():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autores ORDER BY Nome_autor")
    autores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('autores_lista.html', autores=autores)

@app.route('/autores/novo', methods=['GET', 'POST'])
def novo_autor():
    if request.method == 'POST':
        dados = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia) VALUES (%s, %s, %s, %s)"
        valores = (dados['Nome_autor'], dados['Nacionalidade'] or None, dados['Data_nascimento'] or None, dados['Biografia'] or None)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_autores'))
    return render_template('autores_form.html', autor=None, titulo="Novo Autor")

@app.route('/autores/editar/<int:id>', methods=['GET', 'POST'])
def editar_autor(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.form
        sql = """
        UPDATE Autores SET 
            Nome_autor = %s, Nacionalidade = %s, Data_nascimento = %s, Biografia = %s
        WHERE ID_autor = %s
        """
        valores = (dados['Nome_autor'], dados['Nacionalidade'] or None, dados['Data_nascimento'] or None, dados['Biografia'] or None, id)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_autores'))

    cursor.execute("SELECT * FROM Autores WHERE ID_autor = %s", (id,))
    autor = cursor.fetchone()
    cursor.close()
    conn.close()
    if autor is None: return "Autor não encontrado.", 404
    return render_template('autores_form.html', autor=autor, titulo="Editar Autor")

@app.route('/autores/excluir/<int:id>', methods=['POST'])
def excluir_autor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Autores WHERE ID_autor = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_autores'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_autores'))

# -------------------------------------------------------------------
# --- CRUD: GENEROS
# -------------------------------------------------------------------

@app.route('/generos')
def listar_generos():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Generos ORDER BY Nome_genero")
    generos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('generos_lista.html', generos=generos)

@app.route('/generos/novo', methods=['GET', 'POST'])
def novo_genero():
    if request.method == 'POST':
        nome = request.form['Nome_genero']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Generos (Nome_genero) VALUES (%s)", (nome,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_generos'))
    return render_template('generos_form.html', genero=None, titulo="Novo Gênero")

@app.route('/generos/editar/<int:id>', methods=['GET', 'POST'])
def editar_genero(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        nome = request.form['Nome_genero']
        cursor.execute("UPDATE Generos SET Nome_genero = %s WHERE ID_genero = %s", (nome, id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_generos'))
    
    cursor.execute("SELECT * FROM Generos WHERE ID_genero = %s", (id,))
    genero = cursor.fetchone()
    cursor.close()
    conn.close()
    if genero is None: return "Gênero não encontrado.", 404
    return render_template('generos_form.html', genero=genero, titulo="Editar Gênero")

@app.route('/generos/excluir/<int:id>', methods=['POST'])
def excluir_genero(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Generos WHERE ID_genero = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_generos'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_generos'))

# -------------------------------------------------------------------
# --- CRUD: EDITORAS
# -------------------------------------------------------------------

@app.route('/editoras')
def listar_editoras():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Editoras ORDER BY Nome_editora")
    editoras = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('editoras_lista.html', editoras=editoras)

@app.route('/editoras/novo', methods=['GET', 'POST'])
def nova_editora():
    if request.method == 'POST':
        dados = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO Editoras (Nome_editora, Endereco_editora) VALUES (%s, %s)"
        valores = (dados['Nome_editora'], dados['Endereco_editora'] or None)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_editoras'))
    return render_template('editoras_form.html', editora=None, titulo="Nova Editora")

@app.route('/editoras/editar/<int:id>', methods=['GET', 'POST'])
def editar_editora(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.form
        sql = "UPDATE Editoras SET Nome_editora = %s, Endereco_editora = %s WHERE ID_editora = %s"
        valores = (dados['Nome_editora'], dados['Endereco_editora'] or None, id)
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_editoras'))

    cursor.execute("SELECT * FROM Editoras WHERE ID_editora = %s", (id,))
    editora = cursor.fetchone()
    cursor.close()
    conn.close()
    if editora is None: return "Editora não encontrada.", 404
    return render_template('editoras_form.html', editora=editora, titulo="Editar Editora")

@app.route('/editoras/excluir/<int:id>', methods=['POST'])
def excluir_editora(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Editoras WHERE ID_editora = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_editoras'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_editoras'))

# -------------------------------------------------------------------
# --- CRUD: USUARIOS
# -------------------------------------------------------------------

@app.route('/usuarios')
def listar_usuarios():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios ORDER BY Nome_usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios_lista.html', usuarios=usuarios)

@app.route('/usuarios/novo', methods=['GET', 'POST'])
def novo_usuario():
    if request.method == 'POST':
        dados = request.form
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
        INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual) 
        VALUES (%s, %s, %s, %s, %s)
        """
        valores = (
            dados['Nome_usuario'], 
            dados['Email'] or None, 
            dados['Numero_telefone'] or None, 
            dados['Data_inscricao'] or None,
            dados['Multa_atual'] or 0.00
        )
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_usuarios'))
    return render_template('usuarios_form.html', usuario=None, titulo="Novo Usuário")

@app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.form
        sql = """
        UPDATE Usuarios SET 
            Nome_usuario = %s, Email = %s, Numero_telefone = %s, 
            Data_inscricao = %s, Multa_atual = %s
        WHERE ID_usuario = %s
        """
        valores = (
            dados['Nome_usuario'], 
            dados['Email'] or None, 
            dados['Numero_telefone'] or None, 
            dados['Data_inscricao'] or None,
            dados['Multa_atual'] or 0.00,
            id
        )
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    cursor.execute("SELECT * FROM Usuarios WHERE ID_usuario = %s", (id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    if usuario is None: return "Usuário não encontrado.", 404
    return render_template('usuarios_form.html', usuario=usuario, titulo="Editar Usuário")

@app.route('/usuarios/excluir/<int:id>', methods=['POST'])
def excluir_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Usuarios WHERE ID_usuario = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_usuarios'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_usuarios'))

# -------------------------------------------------------------------
# --- CRUD: LIVROS (com chaves estrangeiras)
# -------------------------------------------------------------------

def _get_dados_formulario_livro(conn):
    """Função auxiliar para buscar dados das tabelas FK (Autores, Generos, Editoras)."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID_autor, Nome_autor FROM Autores ORDER BY Nome_autor")
    autores = cursor.fetchall()
    cursor.execute("SELECT ID_genero, Nome_genero FROM Generos ORDER BY Nome_genero")
    generos = cursor.fetchall()
    cursor.execute("SELECT ID_editora, Nome_editora FROM Editoras ORDER BY Nome_editora")
    editoras = cursor.fetchall()
    cursor.close()
    return autores, generos, editoras

@app.route('/livros')
def listar_livros():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    sql = """
    SELECT 
        L.ID_livro, L.Titulo, L.ISBN, L.Ano_publicacao, L.Quantidade_disponivel,
        A.Nome_autor, G.Nome_genero, E.Nome_editora
    FROM Livros L
    LEFT JOIN Autores A ON L.Autor_id = A.ID_autor
    LEFT JOIN Generos G ON L.Genero_id = G.ID_genero
    LEFT JOIN Editoras E ON L.Editora_id = E.ID_editora
    ORDER BY L.Titulo
    """
    cursor.execute(sql)
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('livros_lista.html', livros=livros)

@app.route('/livros/novo', methods=['GET', 'POST'])
def novo_livro():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    
    if request.method == 'POST':
        dados = request.form
        sql = """
        INSERT INTO Livros (
            Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, 
            Editora_id, Quantidade_disponivel, Resumo
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['Titulo'], dados['Autor_id'] or None, dados['ISBN'],
            dados['Ano_publicacao'] or None, dados['Genero_id'] or None,
            dados['Editora_id'] or None, dados['Quantidade_disponivel'] or 0,
            dados['Resumo'] or None
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_livros'))

    autores, generos, editoras = _get_dados_formulario_livro(conn)
    conn.close()
    return render_template('livros_form.html', 
                           livro=None, titulo="Novo Livro",
                           autores=autores, generos=generos, editoras=editoras)

@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    
    if request.method == 'POST':
        dados = request.form
        sql = """
        UPDATE Livros SET
            Titulo = %s, Autor_id = %s, ISBN = %s, Ano_publicacao = %s, Genero_id = %s,
            Editora_id = %s, Quantidade_disponivel = %s, Resumo = %s
        WHERE ID_livro = %s
        """
        valores = (
            dados['Titulo'], dados['Autor_id'] or None, dados['ISBN'],
            dados['Ano_publicacao'] or None, dados['Genero_id'] or None,
            dados['Editora_id'] or None, dados['Quantidade_disponivel'] or 0,
            dados['Resumo'] or None, id
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('listar_livros'))

    autores, generos, editoras = _get_dados_formulario_livro(conn)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Livros WHERE ID_livro = %s", (id,))
    livro = cursor.fetchone()
    cursor.close()
    conn.close()
    if livro is None: return "Livro não encontrado.", 404
    return render_template('livros_form.html', 
                           livro=livro, titulo="Editar Livro",
                           autores=autores, generos=generos, editoras=editoras)

@app.route('/livros/excluir/<int:id>', methods=['POST'])
def excluir_livro(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Livros WHERE ID_livro = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_livros'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_livros'))

# -------------------------------------------------------------------
# --- CRUD: EMPRESTIMOS (com chaves estrangeiras)
# -------------------------------------------------------------------

def _get_dados_formulario_emprestimo(conn):
    """Função auxiliar para buscar dados das tabelas FK (Usuarios, Livros)."""
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT ID_usuario, Nome_usuario FROM Usuarios ORDER BY Nome_usuario")
    usuarios = cursor.fetchall()
    # Idealmente, aqui você filtraria livros com Quantidade_disponivel > 0
    cursor.execute("SELECT ID_livro, Titulo FROM Livros ORDER BY Titulo")
    livros = cursor.fetchall()
    cursor.close()
    return usuarios, livros

@app.route('/emprestimos')
def listar_emprestimos():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    cursor = conn.cursor(dictionary=True)
    sql = """
    SELECT 
        E.ID_emprestimo, E.Data_emprestimo, E.Data_devolucao_prevista, 
        E.Data_devolucao_real, E.Status_emprestimo,
        U.Nome_usuario,
        L.Titulo
    FROM Emprestimos E
    LEFT JOIN Usuarios U ON E.Usuario_id = U.ID_usuario
    LEFT JOIN Livros L ON E.Livro_id = L.ID_livro
    ORDER BY E.Data_emprestimo DESC
    """
    cursor.execute(sql)
    emprestimos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('emprestimos_lista.html', emprestimos=emprestimos)

@app.route('/emprestimos/novo', methods=['GET', 'POST'])
def novo_emprestimo():
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    
    if request.method == 'POST':
        dados = request.form
        sql = """
        INSERT INTO Emprestimos (
            Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, 
            Data_devolucao_real, Status_emprestimo
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        valores = (
            dados['Usuario_id'] or None, 
            dados['Livro_id'] or None,
            dados['Data_emprestimo'] or None,
            dados['Data_devolucao_prevista'] or None,
            dados['Data_devolucao_real'] or None,
            dados['Status_emprestimo']
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        # TODO: Em um app real, você deveria decrementar a Quantidade_disponivel do livro
        cursor.close()
        conn.close()
        return redirect(url_for('listar_emprestimos'))

    usuarios, livros = _get_dados_formulario_emprestimo(conn)
    conn.close()
    return render_template('emprestimos_form.html', 
                           emprestimo=None, titulo="Novo Empréstimo",
                           usuarios=usuarios, livros=livros)

@app.route('/emprestimos/editar/<int:id>', methods=['GET', 'POST'])
def editar_emprestimo(id):
    conn = get_db_connection()
    if not conn: return "Erro de conexão.", 500
    
    if request.method == 'POST':
        dados = request.form
        sql = """
        UPDATE Emprestimos SET
            Usuario_id = %s, Livro_id = %s, Data_emprestimo = %s, 
            Data_devolucao_prevista = %s, Data_devolucao_real = %s, Status_emprestimo = %s
        WHERE ID_emprestimo = %s
        """
        valores = (
            dados['Usuario_id'] or None, 
            dados['Livro_id'] or None,
            dados['Data_emprestimo'] or None,
            dados['Data_devolucao_prevista'] or None,
            dados['Data_devolucao_real'] or None,
            dados['Status_emprestimo'],
            id
        )
        cursor = conn.cursor()
        cursor.execute(sql, valores)
        conn.commit()
        # TODO: Se o status mudou para 'devolvido', incrementar Quantidade_disponivel
        cursor.close()
        conn.close()
        return redirect(url_for('listar_emprestimos'))

    usuarios, livros = _get_dados_formulario_emprestimo(conn)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Emprestimos WHERE ID_emprestimo = %s", (id,))
    emprestimo = cursor.fetchone()
    cursor.close()
    conn.close()
    if emprestimo is None: return "Empréstimo não encontrado.", 404
    return render_template('emprestimos_form.html', 
                           emprestimo=emprestimo, titulo="Editar Empréstimo",
                           usuarios=usuarios, livros=livros)

@app.route('/emprestimos/excluir/<int:id>', methods=['POST'])
def excluir_emprestimo(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM Emprestimos WHERE ID_emprestimo = %s", (id,))
        conn.commit()
    except mysql.connector.Error as err:
        return handle_db_error(err, url_for('listar_emprestimos'))
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('listar_emprestimos'))

# --- Execução da Aplicação ---
if __name__ == '__main__':
    app.run(debug=True)
