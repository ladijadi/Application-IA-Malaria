import tensorflow as tf
import numpy as np
from PIL import Image
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
model = tf.keras.models.load_model("app/model/malaria_model.keras")

def preprocess_image(image):
    """Prétraitement de l'image téléchargée."""
    image = image.resize((128, 128))
    image = np.array(image) / 255.0  # Normaliser entre 0 et 1
    return np.expand_dims(image, axis=0)  # Ajouter une dimension batch

@app.route('/predict', methods=['POST'])
def predict():
    """Prédiction à partir d'une image téléchargée."""
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier envoyé."}), 400
    file = request.files['file']
    try:
        image = Image.open(file.stream)
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        label = "Infectée" if prediction < 0.5 else "Non infectée"
        return jsonify({"prediction": label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)