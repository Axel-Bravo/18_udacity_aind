
def main():
    import numpy as np
    from keras.utils import np_utils
    import tensorflow as tf
    # Using TensorFlow 1.0.0; use tf.python_io in later versions
    tf.python_io.control_flow_ops = tf

    # Set random seed
    np.random.seed(42)

    #%% Data Generation
    # Our data
    X = np.array([[0,0],[0,1],[1,0],[1,1]]).astype('float32')
    y = np.array([[0],[1],[1],[0]]).astype('float32')

    # Initial Setup for Keras
    from keras.models import Sequential
    from keras.layers.core import Dense, Activation

    #%% Model Creation
    # Building the model
    xor = Sequential()

    # Add required layers
    # xor.add()
    xor.add(Dense(8,  input_shape=(2, )))
    xor.add(Activation('tanh'))
    xor.add(Dense(1))
    xor.add(Activation('sigmoid'))

    # Specify loss as "binary_crossentropy", optimizer as "adam",
    # and add the accuracy metric
    # xor.compile()
    xor.compile(optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy'],
                )

    # Uncomment this line to print the model architecture
    # xor.summary()
    xor.summary()

    #%% Model Fitting and plotting

    #  Fitting the model
    history = xor.fit(X, y, epochs=1000, verbose=0)

    # Scoring the model
    score = xor.evaluate(X, y)
    print("\nAccuracy: ", score[-1])

    # Checking the predictions
    print("\nPredictions:")
    print(xor.predict_proba(X))


if __name__ == '__main__':
    main()