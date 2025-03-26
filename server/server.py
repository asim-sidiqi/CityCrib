from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/gln')
def get_locations():
    output = jsonify(util.get_location_names())
    return output

@app.route('/elp', methods=['POST'])
def predict_estimated_price():
    location = request.form['location']
    total_sqft = float(request.form['total_sqft'])
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    response = jsonify(util.get_estimated_price(location, total_sqft, bhk, bath))
    return response

if __name__ == "__main__":
    print("Flask server running...")
    app.run()
