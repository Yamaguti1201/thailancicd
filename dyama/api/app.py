import os
import time
from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

STUDENT_NAME = os.getenv("STUDENT_NAME", "Dyama")
SITE_DOMAIN = os.getenv("DOMAIN", "devops007.ugbio.com.br")

def get_db_connection(retries=15, delay=2):
    for attempt in range(retries):
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "devops_user"),
                password=os.getenv("DB_PASSWORD", "devops123_site4"),
                database=os.getenv("DB_NAME", "devopsdb_site4"),
                port=int(os.getenv("DB_PORT", "3306")),
                connection_timeout=5,
            )
        except Error as err:
            if attempt == retries - 1:
                raise err
            time.sleep(delay)

def initialize_database():
    try:
        connection = get_db_connection(retries=10, delay=2)
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                author VARCHAR(100) NOT NULL,
                content VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        
        # Inserir registro inicial se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        if count == 0:
            cursor.execute(
                "INSERT INTO messages (author, content) VALUES (%s, %s)",
                (STUDENT_NAME, f"Inicialização da API devops007 - Integrado com MySQL e Nginx!")
            )
            connection.commit()

        cursor.close()
        connection.close()
    except Exception as e:
        print(f"Aviso durante inicialização do banco: {e}")

# Executa inicialização
try:
    initialize_database()
except Exception as e:
    print(f"Erro inicializando banco: {e}")

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "disciplina": "DevOps - UGB",
        "exercicio": "CI/CD com Containers (Site 4)",
        "aluno": STUDENT_NAME,
        "dominio": SITE_DOMAIN,
        "arquitetura": {
            "dns": "Cloudflare HTTP 80",
            "proxy": "Nginx",
            "backend": "Python Flask (Imagem API)",
            "banco": "MySQL 8.4"
        },
        "endpoints": [
            {"metodo": "GET", "rota": "/", "descricao": "Informações gerais da API"},
            {"metodo": "GET", "rota": "/health", "descricao": "Healthcheck da API e conexão MySQL"},
            {"metodo": "GET", "rota": "/mensagens", "descricao": "Lista mensagens cadastradas no MySQL"},
            {"metodo": "POST", "rota": "/mensagens", "descricao": "Cadastra nova mensagem (JSON: {'author': '...', 'content': '...'})"}
        ]
    })

@app.route("/health")
def health():
    try:
        conn = get_db_connection(retries=1)
        conn.close()
        return jsonify({
            "status": "healthy",
            "service": "api",
            "database": "connected",
            "aluno": STUDENT_NAME,
            "site": SITE_DOMAIN
        }), 200
    except Error as exc:
        return jsonify({
            "status": "unhealthy",
            "service": "api",
            "database": "disconnected",
            "error": str(exc)
        }), 503

@app.route("/mensagens", methods=["GET"])
def list_messages():
    try:
        conn = get_db_connection(retries=3)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, author, content, created_at FROM messages ORDER BY id DESC")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            if row.get("created_at"):
                row["created_at"] = row["created_at"].isoformat()
        return jsonify({"aluno": STUDENT_NAME, "total": len(rows), "mensagens": rows}), 200
    except Exception as e:
        return jsonify({"error": "Erro ao consultar mensagens no MySQL", "details": str(e)}), 500

@app.route("/mensagens", methods=["POST"])
def create_message():
    data = request.get_json(silent=True) or {}
    content = data.get("content")
    author = data.get("author", STUDENT_NAME)
    
    if not isinstance(content, str) or not content.strip():
        return jsonify({"error": "O campo 'content' é obrigatório e não pode ser vazio."}), 400

    try:
        conn = get_db_connection(retries=3)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (author, content) VALUES (%s, %s)", (author.strip(), content.strip()))
        conn.commit()
        message_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({
            "mensagem": "Registro inserido com sucesso no MySQL!",
            "id": message_id,
            "author": author,
            "content": content.strip()
        }), 201
    except Exception as e:
        return jsonify({"error": "Falha ao gravar no MySQL", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
