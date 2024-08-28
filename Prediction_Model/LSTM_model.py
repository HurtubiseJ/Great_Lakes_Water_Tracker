import keras 
import numpy as np 
import pathlib  
import pandas as pd
from keras._tf_keras.keras.layers import Activation, Dropout, Flatten, Dense
from sklearn.model_selection import TimeSeriesSplit
import math
from sklearn import preprocessing as pre
import matplotlib.pyplot as plt


data_csv_path = pathlib.Path('C:\\Users\\jhurt\\OneDrive\\Desktop\\Great_Lakes_Water_Tracker\\Prediction_Model\\CO-OPS_9014090_wl.csv')

def min_max_normalize(data):
    min_val = np.min(data)
    max_val = np.max(data)
    return (data - min_val) / (max_val - min_val), min_val, max_val

def unnormalize(data, min_val, max_val):
    return data * (max_val - min_val) + min_val

def get_training_data():
    try: 
        return pd.read_csv(data_csv_path).drop(['Predicted (ft)', 'Preliminary (ft)', 'Time (LST/LDT)', 'Date'], axis=1) #Read and drop not used data
    except: 
        print("Failed to read in training Data.")

def create_single_layer_LSTM(single_layer_size, X_pretrain_for_shape, loss):
    lstm_model = keras.Sequential()
    # lstm_model.add(keras.layers.LSTM(single_layer_size, Input=keras.Input(1, X_pretrain_for_shape.shape[1]), activation="relu", return_sequences=False))
    lstm_model.add(keras.layers.LSTM(single_layer_size, input_shape=(1, X_pretrain_for_shape.shape[1]), activation="relu", return_sequences=False))
    lstm_model.add(Dense(1))
    lstm_model.compile(loss=loss, optimizer="adam")
    return lstm_model

def partitionData(feature_transform, output_var):
    timesplit = TimeSeriesSplit(n_splits=10)
    for train_index, test_index in timesplit.split(feature_transform):
        X_train, X_test = feature_transform[:len(train_index)], feature_transform[len(train_index): (len(train_index)+len(test_index))]
        y_train, y_test = output_var[:len(train_index)].values.ravel(), output_var[len(train_index): (len(train_index)+len(test_index))].values.ravel()

    return X_train, X_test, y_train, y_test

#Using 90-10 training to test split
def partition_and_shape(df):
    trainLen = math.floor(df.shape[0] * 0.9)
    ary = np.array(df)
    x_train = min_max_normalize(ary[:trainLen])
    y_test = min_max_normalize(ary[trainLen:])
    x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1])
    y_test = y_test.reshape(y_test.shape[0], 1, y_test.shape[1])
    return x_train, y_test

def format_test_data(x_train):
    x_test = np.append(x_train[1:], x_train[len(x_train)-1])
    return x_test.reshape(x_test.shape[0], 1, 1)

def plot_performance(hist, metrics = ["loss"]):
  epochs = 40
  ax = plt.gca()
  i = 0
  name = ['Water Level Prediction']
  for metric in metrics:
    ax.set_ylim([0, 3])
    ax.plot([i-.5 for i in range(1,epochs+1)], hist.history[metric], label=name[i]+ " Train " + metric)
    ax.plot(range(1,epochs+1), hist.history[ metric], label=name[i]+" Validation " + metric)
    ax.legend()
    i+=1

    plt.xlabel("Epoch")
    plt.ylabel(metric)
    plt.title(metric.capitalize() + " over time")
    plt.show()

def create_prediction_plots(y_predictions, y_test):
  plt.plot(y_test, label="True Value")
#   for i in range(len(y_predictions)):
  plt.plot(y_predictions, label="Model Value")
  plt.legend()

  plt.title("Prediction by LSTM")
  plt.xlabel("Time Scale")
  plt.ylabel("Scaled USD")
  plt.show()

def main():
    df = get_training_data()
    x_train, y_test = partition_and_shape(df)
    x_test = format_test_data(x_train)
    print(x_train.shape)
    print(x_train)
    print(x_test.shape)
    print(x_test)
    model = create_single_layer_LSTM(20, x_train, "mean_squared_error")
    histories = model.fit(x_train, x_test, epochs=40, batch_size=24, verbose=1, shuffle=False)
    pred = model.predict(y_test)
    plot_performance(histories)
    pred = unnormalize(pred)
    y_test = unnormalize(y_test)
    create_prediction_plots(pred, y_test)
    print(model)


if __name__ == '__main__':
    main()