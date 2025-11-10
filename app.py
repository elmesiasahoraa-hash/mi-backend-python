from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"mensaje": "Servidor funcionando correctamente 🟢"})

@app.route('/datos', methods=['POST'])
def recibir_datos():
    data = request.get_json()
    print("Datos recibidos:", data)
    return jsonify({"status": "ok", "data": data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
