# models/operacion.py
from .db import get_connection

class Operacion:
    @staticmethod
    def guardar(a, b, operacion, resultado):
        """
        Guarda una operación en la base de datos.
        a, b: números
        operacion: str ("sumar", "restar", "multiplicar", "dividir")
        resultado: float
        """
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO operaciones (a, b, operacion, resultado) VALUES (%s, %s, %s, %s)",
            (a, b, operacion, resultado)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_historial(limite=10):
        """
        Obtiene las últimas operaciones de la base de datos.
        limite: cantidad de registros a retornar
        """
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM operaciones ORDER BY id DESC LIMIT {limite}")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
