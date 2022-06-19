from tensorflow import keras


def build_model():
    model = keras.models.Sequential()
    model.add(keras.layers.Dense(16, activation='relu', input_shape=(5,)))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    return model
