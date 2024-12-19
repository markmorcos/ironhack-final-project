from flask import Flask, request, jsonify
from flask_cors import CORS
import pretty_midi
import pandas as pd
import joblib

import feature_engineering

app = Flask(__name__)
CORS(app)

@app.route("/predict", methods=["GET"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    file_path = f"/tmp/{file.filename}"
    file_path = "./data/raw/2018/MIDI-Unprocessed_Schubert10-12_MID--AUDIO_20_R2_2018_wav.midi"

    try:
        midi_data = pretty_midi.PrettyMIDI(file_path)
        data = feature_engineering.extract_midi_features(midi_data)
        features = pd.DataFrame(data, index=[0])
        
        model = joblib.load("./data/models/rf.joblib")
        era = model.predict(features)[0]

        return jsonify({"era": era}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
