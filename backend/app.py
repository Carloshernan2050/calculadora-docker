from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import mysql.connector as mysql

app = Flask(__name__)

# 🔹 CORS global
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True,
    allow_headers="*",
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)

# Conexión a MySQL
def get_connection():
    return mysql.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "root"),
        database=os.getenv("DB_NAME", "calculadora")
    )

# Historial en DB
@app.route("/operacion", methods=["POST"])
def operacion():
    data = request.get_json()
    a = data.get("a", 0)
    b = data.get("b", 0)
    op = data.get("op")

    if op == "sumar":
        resultado = a + b
    elif op == "restar":
        resultado = a - b
    elif op == "multiplicar":
        resultado = a * b
    elif op == "dividir":
        resultado = a / b if b != 0 else None
    else:
        return jsonify({"error": "Operación inválida"}), 400

    # Guardar en DB
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "INSERT INTO operaciones (a, b, operacion, resultado) VALUES (%s, %s, %s, %s)",
        (a, b, op, resultado)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"resultado": resultado})

@app.route("/historial", methods=["GET"])
def historial():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT a, b, operacion, resultado FROM operaciones ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)

@app.route("/")
def index():
    return "API Calculadora funcionando", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
