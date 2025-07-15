import json
import pickle
import numpy as np

data_columns_ = None
model_ = None

def get_estimated_price(location, total_sqft, bath, bhk):
    global data_columns_, model_

    try:
        loc = data_columns_.index(location.lower())
    except:
        loc = -1

    X = np.zeros(len(data_columns_))
    X[0] = total_sqft
    X[1] = bath
    X[2] = bhk

    if loc >= 0:
        X[loc] = 1
    return round(model_.predict([X])[0], 2)

def load_artifacts():
    global data_columns_, model_

    print("Loading model and columns...")
    with open('./artifacts/columns.json', 'r') as f:
        data_columns_ = json.load(f)['data_columns']

    with open('./artifacts/bangalore_home_prices_model.pickle', 'rb') as f:
        model_ = pickle.load(f)

    print("Artifacts loaded successfully.")

def get_location_names():
    global data_columns_
    return data_columns_[3:]  # Skip sqft, bath, bhk

if __name__ == '__main__':
    load_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
