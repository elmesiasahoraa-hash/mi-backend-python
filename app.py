from flask import Flask, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# === CONFIGURAR CONEXIÓN A GOOGLE SHEETS ===
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

# 🔹 Cambiá por el ID de tu hoja
SPREADSHEET_ID = "1T4AE9sEqgvDm7gcI5CD5MOpy4LMB1aS1IbVzc_T27GQ"

@app.route("/", methods=["GET"])
def home():
    tipo = request.args.get("tipo", "")

    if tipo == "syncBajarPedidos":
        hoja = client.open_by_key(SPREADSHEET_ID).worksheet("datos")
        data = hoja.get_all_records()
        return jsonify({"pedidos": data})

    elif tipo == "syncBajarCompras":
        hoja = client.open_by_key(SPREADSHEET_ID).worksheet("compras")
        data = hoja.get_all_records()
        return jsonify({"compras": data})

    elif tipo == "syncBajarStock":
        hoja = client.open_by_key(SPREADSHEET_ID).worksheet("stock_bizcocho")
        data = hoja.get_all_records()
        return jsonify({"stock": data})

    else:
        return jsonify({"error": "Tipo no reconocido"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
