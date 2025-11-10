from flask import Flask, request, jsonify
from flask_cors import CORS  # <--- Importante
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)
CORS(app)  # <--- Habilita CORS para todas las rutas

# Configurar conexión a Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credenciales.json", scopes=SCOPES)
gc = gspread.authorize(creds)

# ID de tu hoja (copialo desde la URL)
SHEET_ID = "1T4AE9sEqgvDm7gcI5CD5MOpy4LMB1aS1IbVzc_T27GQ"

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensaje": "Servidor funcionando correctamente 🟢"})

@app.route("/", methods=["POST"])
def recibir_datos():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400

    tipo = data.get("tipo")

    try:
        sh = gc.open_by_key(SHEET_ID)

        if tipo == "stock_bizcocho":
            ws = sh.worksheet("stock_bizcocho")
            stock = data.get("stock", {})
            ws.append_row([
                stock.get("bizcocho", ""),
                stock.get("embuche", ""),
                stock.get("neutro", ""),
                stock.get("fecha", "")
            ])
            return jsonify({"ok": True, "mensaje": "Stock guardado"})

        elif tipo == "compras":
            ws = sh.worksheet("compras")
            compra = data.get("compra", {})
            ws.append_row([
                compra.get("producto", ""),
                compra.get("cantidad", ""),
                compra.get("fecha", "")
            ])
            return jsonify({"ok": True, "mensaje": "Compra guardada"})

        else:
            return jsonify({"error": "Tipo de datos desconocido"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
