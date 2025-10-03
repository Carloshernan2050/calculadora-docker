from .db import get_connection

class Operacion:
    @staticmethod
    def guardar(num1, num2, operacion, resultado):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO operaciones (num1, num2, operacion, resultado) VALUES (%s, %s, %s, %s)",
            (num1, num2, operacion, str(resultado))
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def obtener_historial():
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM operaciones ORDER BY id DESC LIMIT 10")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
