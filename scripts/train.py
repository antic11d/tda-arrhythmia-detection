# %%
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import argparse

from sklearn.model_selection import train_test_split

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Conv1D, GlobalMaxPooling1D, Flatten, MaxPooling1D, PReLU
from keras.initializers import Constant


# %%
def evaluate_model(train_x, train_y, test_x, test_y, dropout, epochs, batch_size, model_save):
    model = Sequential()

    model.add(Conv1D(filters=64, kernel_size=5, input_shape=(train_x.shape[1], 1), padding='same'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(PReLU(alpha_initializer=Constant(value=0.25)))
    model.add(Dropout(dropout))

    model.add(Conv1D(filters=128, kernel_size=5, padding='same'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(PReLU(alpha_initializer=Constant(value=0.25)))
    model.add(Dropout(dropout))

    model.add(Conv1D(filters=128, kernel_size=5, padding='same'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(PReLU(alpha_initializer=Constant(value=0.25)))
    model.add(Dropout(dropout))

    model.add(Conv1D(filters=128, kernel_size=3, padding='same'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(PReLU(alpha_initializer=Constant(value=0.25)))
    model.add(Dropout(dropout))

    model.add(Flatten())
    model.add(Dense(30))
    model.add(PReLU(alpha_initializer=Constant(value=0.25)))
    model.add(Dense(2, activation='softmax'))


    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    # fit network
    history = model.fit(train_x, train_y, epochs=epochs, batch_size=batch_size, verbose=1)
    # evaluate model
    loss, accuracy = model.evaluate(test_x, test_y, batch_size=batch_size, verbose=0)

    model.save(model_save)
    return history, accuracy, loss

# %%
def visualize_history(history):
    plt.plot(history.history['accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train accuracy', 'train loss'], loc='upper left')
    plt.show()
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

# %%
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', help='Relative path to the data folder')
    parser.add_argument('--model_path', help='Relative path to the model saving location')
    parser.add_argument('--epochs', type=int, help='Number of epochs')
    parser.add_argument('--test_size', type=float, help='Percentage of data used for test')
    parser.add_argument('--dropout', type=float, help='Dropout percentage')
    parser.add_argument('--batch_size', type=int, help='Batch size')
    args = parser.parse_args()

    df = pd.read_csv(args.data_path)
    X = df.iloc[:, :-1]
    y = df['class']
    y = to_categorical(y)

    X = np.expand_dims(X, axis=2)

    train_x, test_x, train_y, test_y = train_test_split(X, y, test_size=args.test_size, stratify=y, random_state=42)
    train_history, test_accuracy, test_loss = evaluate_model(train_x, train_y, test_x, test_y, args.dropout, args.epochs, args.batch_size, args.model_path)

    print(f'Test accuracy: {test_accuracy}')




# %%
if __name__ == '__main__':
    main()


# %%


