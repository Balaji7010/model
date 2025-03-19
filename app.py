from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import logging

app = Flask(__name__, template_folder='templates')
CORS(app)  # Allow frontend requests from different origins

logging.basicConfig(level=logging.INFO)  # Enable logging for debugging

# Initial status data
status_data = {
    "driverStatus": "Active",
    "eyeStatus": "Open",
    "drowsinessLevel": "Low",
    "drowsinessAlert": "No Alert",
    "blindSpotStatus": "Clear",
    "gps": {"latitude": 12.879080, "longitude": 79.122219}
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(status_data)

@app.route('/update_status', methods=['POST'])
def update_status():
    try:
        new_status = request.get_json()
        if not new_status:
            return jsonify({"error": "Invalid request data"}), 400

        # Update only known keys to prevent errors
        for key in status_data.keys():
            if key in new_status:
                status_data[key] = new_status[key]

        logging.info(f"Updated status: {status_data}")
        return jsonify({"message": "Status updated successfully", "status": status_data}), 200

    except Exception as e:
        logging.error(f"Error updating status: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running"}), 200

# ✅ New route to serve dha.html
@app.route('/3d-model')
def three_d_model():
    return render_template('dha.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
