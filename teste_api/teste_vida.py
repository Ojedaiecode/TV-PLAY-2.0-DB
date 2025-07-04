from flask import Flask, jsonify
import os

# Ativa modo debug do Flask
os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)

@app.route("/status")
def status():
    return jsonify({"status": "Backend com Flask funcionando direto"})
    
if __name__ == "__main__":
    # Inicia com host e porta do Railway
    app.run(host="0.0.0.0", port=8080) 