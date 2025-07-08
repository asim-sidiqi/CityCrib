import json
import pickle
import numpy as np

locations_ = None
data_columns_ = None
model_= None

def get_estimated_price(location, total_sqft, bath, bhk):
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
    return round(model_.predict([X])[0],2)

def get_location_names():
    global locations_
    global data_columns_
    global model_

    print('getting data....start')
    with open('./artifacts/columns.json', 'r') as f:
        data_columns_ = json.load(f)['data_columns']
        location_ = data_columns_[3:]

    with open('./artifacts/bangalore_home_prices_model.pickle', 'rb') as model:
        model_ = pickle.load(model)

    print('getting data....done')
    return location_


if __name__ == '__main__':
    print(get_location_names())
    print(get_estimated_price( '1st Phase JP Nagar',1000,3,3))