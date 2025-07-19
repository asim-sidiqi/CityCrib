from flask import Flask, request, jsonify
from flask_cors import CORS
from . import util

app = Flask(__name__)
CORS(app)

@app.route('/api/get_location_names', methods=['GET'])
def get_locations():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    try:
        util.load_artifacts(city)
        locations = util.get_location_names(city)
        return jsonify({ "locations": locations })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/predict_home_price', methods=['POST'])
def predict_estimated_price():
    data = request.get_json()
    city = data.get('city')
    location = data.get('location')
    total_sqft = float(data.get('total_sqft'))
    bhk = int(data.get('bhk'))
    bath = int(data.get('bath'))

    if not city:
        return jsonify({"error": "City is required"}), 400

    try:
        util.load_artifacts(city)
        estimated_price = util.get_estimated_price(city, location, total_sqft, bath, bhk)
        return jsonify({ "estimated_price": estimated_price })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Flask server running...")
    app.run(debug=True)
