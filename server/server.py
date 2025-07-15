from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)

@app.route('/api/get_location_names', methods=['GET'])
def get_locations():
    locations = util.get_location_names()
    return jsonify({ "locations": locations })

@app.route('/api/predict_home_price', methods=['POST'])
def predict_estimated_price():
    data = request.get_json()
    location = data['location']
    total_sqft = float(data['total_sqft'])
    bhk = int(data['bhk'])
    bath = int(data['bath'])

    estimated_price = util.get_estimated_price(location, total_sqft, bath, bhk)
    return jsonify({ "estimated_price": estimated_price })

if __name__ == "__main__":
    print("Flask server running...")
    util.load_artifacts()
    app.run(debug=True)
