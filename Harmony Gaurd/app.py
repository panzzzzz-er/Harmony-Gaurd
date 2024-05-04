from flask import Flask, render_template, request, jsonify
import os
from pydub import AudioSegment
import io
import sounddevice as sd
import numpy as np
import librosa

# Import your custom Keras model and preprocessing function
from keras.models import load_model

# Initialize Flask app
app = Flask(__name__, template_folder='templates')

# Load your trained Keras model
model = load_model("path_to_your_saved_model.h5")

# Function to convert MP3 to FLAC
def convert_mp3_to_flac(mp3_data):
    audio = AudioSegment.from_mp3(io.BytesIO(mp3_data))
    flac_data = audio.export(format="flac").read()
    return flac_data

# Function to preprocess audio data
def preprocess_audio(file_path, target_duration=20):
    audio, _ = librosa.load(file_path, sr=None)
    target_length = int(target_duration * _)

    if len(audio) < target_length:
        audio = np.pad(audio, (0, target_length - len(audio)))
    else:
        audio = audio[:target_length]

    # Extract Mel-frequency cepstral coefficients (MFCCs)
    mfccs = librosa.feature.mfcc(y=audio, sr=_, n_mfcc=13)

    return mfccs

# Route to upload audio file
@app.route("/upload", methods=["POST"])
def upload_audio():
    try:
        # Check if the POST request has the file part
        if 'audio' not in request.files:
            return jsonify({"success": False, "error": "No file part"})

        audio_file = request.files['audio']

        # If the user does not select a file, the browser submits an empty part without filename
        if audio_file.filename == '':
            return jsonify({"success": False, "error": "No selected file"})

        if audio_file:
            # Save the uploaded audio file
            audio_file_path = "static/audio/uploaded_audio.mp3"
            audio_file.save(audio_file_path)

            return jsonify({"success": True, "message": "Audio file uploaded successfully", "audio_file_path": audio_file_path})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Route to analyze uploaded audio file
@app.route("/analyze", methods=["POST"])
def analyze_audio():
    try:
        # Get the path of the uploaded audio file
        audio_file_path = request.json.get("audio_file_path")

        if not audio_file_path:
            return jsonify({"success": False, "error": "Audio file path not provided"})

        # Preprocess the uploaded audio
        mfccs = preprocess_audio(audio_file_path)

        # Reshape the input for the model
        input_data = np.expand_dims(mfccs, axis=0)

        # Perform prediction using your trained Keras model
        prediction = model.predict(input_data)

        # Define your threshold
        threshold = 0.5

        # Determine the result based on the threshold
        if prediction > threshold:
            result_text = "Hate Speech Detected"
        else:
            result_text = "No Hate Speech Detected"

        return jsonify({"success": True, "result": result_text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
