import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from keras.utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import Dense
from keras.layers import LSTM
import random as rn

def train_model(x, y):

    sns.set()

    y = to_categorical(y, 128)

    save = tf.keras.callbacks.ModelCheckpoint('weights3.{epoch:02d}-{loss:.2f}.hdf5', monitor='loss', verbose=0,
                                              save_best_only=True, save_weights_only=False, mode='auto', period=1)

    model = Sequential()
    model.add(LSTM(256, input_shape=(1, 3),return_sequences=True))
    model.add(LSTM(256))
    model.add(Dense(512, activation='relu'))
    model.add(Dense(128, activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    history = model.fit(x, y, validation_split=0.2, batch_size=512, epochs=100, callbacks=[save])

    print(model.summary())

    #change this before training a new model
    model.save('model6.h5')

    plt.figure(figsize=(10, 5))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('loss.png', dpi=300)

    test_predict = model.predict(x)

    print(test_predict)

def set_seed():
    # The below is necessary for starting Numpy generated random numbers
    # in a well-defined initial state.

    np.random.seed(42)

    # The below is necessary for starting core Python generated random numbers
    # in a well-defined state.

    rn.seed(12345)

    # Force TensorFlow to use single thread.
    # Multiple threads are a potential source of non-reproducible results.
    # For further details, see: https://stackoverflow.com/questions/42022950/

    session_conf = tf.ConfigProto(intra_op_parallelism_threads=1,
                                  inter_op_parallelism_threads=1)

    from keras import backend as K

    # The below tf.set_random_seed() will make random number generation
    # in the TensorFlow backend have a well-defined initial state.
    # For further details, see:
    # https://www.tensorflow.org/api_docs/python/tf/set_random_seed

    tf.set_random_seed(1234)

    sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
    K.set_session(sess)

    # Rest of code follows ...

def load_dist(x, mod):

    model = load_model(mod)

    return model.predict(x)


