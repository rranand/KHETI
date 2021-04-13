from keras.models import load_model
from keras import preprocessing
import tensorflow as tf
from django.conf import settings

model = load_model(r'weed_removal.h5')


def predict(dire=""):
    path = settings.BASE_DIR / 'images' / dire

    img = preprocessing.image.load_img(
        path, target_size=(180, 180)
    )
    img_array = preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)  # Create batch axis

    predictions = model.predict(img_array)
    score = predictions[0]

    typ = ['broadleaf', 'grass', 'soil', 'soyabean']

    arr = []
    for i in range(4):
        arr.append([score[i], typ[i]])

    arr.sort()
    return arr[3][1] == 'broadleaf'
