import json
import pickle
import numpy as np
import os

# Dictionary to cache loaded models and columns per city
city_artifacts = {}

def load_artifacts(city):
    city = city.lower()
    if city in city_artifacts:
        return city_artifacts[city]

    base_path = os.path.join(os.path.dirname(__file__), "artifacts")
    if not os.path.exists(base_path):
        raise FileNotFoundError("Artifacts directory does not exist")
    model_path = os.path.join(base_path, f"{city}_home_prices_model.pickle")
    column_path = os.path.join(base_path, f"columns_{city}.json")

    if not os.path.exists(model_path) or not os.path.exists(column_path):
        raise FileNotFoundError(f"Artifacts not found for city: {city}")

    with open(column_path, 'r') as f:
        data_columns = json.load(f)['data_columns']

    with open(model_path, 'rb') as f:
        model = pickle.load(f)

    city_artifacts[city] = {
        "columns": data_columns,
        "model": model
    }

    return city_artifacts[city]

def get_location_names(city):
    artifacts = load_artifacts(city)
    return artifacts["columns"][3:]  # Skip sqft, bath, bhk

def get_estimated_price(city, location, total_sqft, bath, bhk):
    artifacts = load_artifacts(city)
    data_columns = artifacts["columns"]
    model = artifacts["model"]

    try:
        loc_index = data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(model.predict([x])[0], 2)

# Debug/test
if __name__ == '__main__':
    print(get_location_names("bangalore"))
    print(get_estimated_price("bangalore", '1st Phase JP Nagar', 1000, 3, 3))
    print(get_location_names("delhi"))
    print(get_estimated_price("delhi", 'saket', 1200, 2, 2))  # Adjust based on actual Delhi localities
