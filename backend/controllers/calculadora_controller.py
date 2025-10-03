from flask import Blueprint, request, jsonify
import mysql.connector
import os

calculadora_bp = Blueprint("calculadora", __name__)

# Configuración de conexión a MySQL usando variables de entorno (coincide con docker-compose.yml)
db_config = {
    "host": os.getenv("DB_HOST", "db"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "database": os.getenv("DB_NAME", "calculadora")
}

def get_connection():
    return mysql.connector.connect(**db_config)

@calculadora_bp.route("/operacion", methods=["POST"])
def operacion():
    data = request.get_json()
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    op = data.get("op", "sumar")

    if op == "sumar":
        resultado = a + b
    elif op == "restar":
        resultado = a - b
    elif op == "multiplicar":
        resultado = a * b
    elif op == "dividir":
        resultado = a / b if b != 0 else "Error: división por cero"
    else:
        return jsonify({"error": "Operación inválida"}), 400

    # Guardar en MySQL
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO operaciones (a, b, operacion, resultado) VALUES (%s,%s,%s,%s)",
        (a, b, op, resultado if isinstance(resultado, (int, float)) else None)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"resultado": resultado})

@calculadora_bp.route("/historial", methods=["GET"])
def historial():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM operaciones ORDER BY id DESC LIMIT 10")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)
