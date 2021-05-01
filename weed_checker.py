import joblib
import numpy as np
from django.conf import settings
from keras import preprocessing
from keras.models import load_model


def predict(dire=""):
    path = settings.BASE_DIR / 'images' / dire

    img = preprocessing.image.load_img(
        path, target_size=(180, 180)
    )
    img_array = preprocessing.image.img_to_array(img)
    img_array = img_array[np.newaxis]

    predictions = load_model(str(settings.BASE_DIR / 'models' / 'weed_removal.h5')).predict(img_array)
    score = predictions[0]

    typ = ['broadleaf', 'grass', 'soil', 'soyabean']

    arr = []
    for i in range(4):
        arr.append([score[i], typ[i]])

    arr.sort()
    return arr[3][1] == 'broadleaf'


def soil_fertilizer_predict(temperature, humidity, moisture, soil, crop, n, k, p):
    soil_dict = {"black": 0, "clayey": 1, "loamy": 2, "red": 3, "sandy": 4}
    crop_dict = {"barley": 0, "cotton": 1, "ground nuts": 2, "maize": 3, "millets": 4, "oil seeds": 5, "paddy": 6,
                 "pulses": 7, "sugarcane": 8, "tobacco": 9, "wheat": 10}

    loaded_model = joblib.load(str(settings.BASE_DIR / 'models' / 'MLP_Fert.sav'))
    s1 = [0] * len(soil_dict)
    t1 = [0] * len(crop_dict)
    s1[soil_dict[soil.lower()]] = 1
    t1[crop_dict[crop.lower()]] = 1
    test = [[temperature, humidity, moisture, n, k, p] + s1 + t1]

    return loaded_model.predict(test)[0]


def crop_recommendations_predict(n, k, p, temperature, humidity, ph, rainfall):
    loaded_model = joblib.load(str(settings.BASE_DIR / 'models' / 'RandomForestModel.sav'))
    test = [[n, p, k, temperature, humidity, ph, rainfall]]

    return loaded_model.predict(test)[0]
