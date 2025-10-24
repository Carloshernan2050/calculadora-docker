from models.operacion import Operacion
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/operacion", methods=["POST"])
def operacion():
    data = request.get_json()
    a = float(data.get("a", 0))
    b = float(data.get("b", 0))
    op = data.get("op", "sumar")

    if op == "sumar":
        res = a + b
    elif op == "restar":
        res = a - b
    elif op == "multiplicar":
        res = a * b
    elif op == "dividir":
        res = a / b if b != 0 else 0
    else:
        res = 0

    Operacion.guardar(a, b, op, res)
    return jsonify({"resultado": res})

@app.route("/historial", methods=["GET"])
def historial():
    rows = Operacion.obtener_historial()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
