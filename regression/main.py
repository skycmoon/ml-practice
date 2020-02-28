import pandas as pd
import math
import quandl
import numpy as np
from sklearn import preprocessing, svm
from sklearn import model_selection
from sklearn.linear_model import LinearRegression


def main():
    df = quandl.get('WIKI/GOOGL')
    df = df[['Adj. Open', 'Adj. High', 'Adj. Low', 'Adj. Close', 'Adj. Volume']]
    df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] * 100
    df['PCT_change'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open'] * 100
    df = df[['Adj. Close', 'HL_PCT', 'PCT_change', 'Adj. Volume']]
    forecast_col = 'Adj. Close'
    df.fillna(-99999, inplace=True)
    forecast_out = int(math.ceil(0.01 * len(df)))  # forecast out 10% of data length.
    df['label'] = df[forecast_col].shift(-forecast_out)
    df.dropna(inplace=True)

    x = np.array(df.drop(['label'], 1))  # features
    y = np.array(df['label'])  # label

    x = preprocessing.scale(x)  # scale before feeding through classifier. scale them alongside other values.
    # x = x[:-forecast_out + 1]
    df.dropna(inplace=True)
    y = np.array(df['label'])

    x_train, x_test, y_train, y_test = model_selection.train_test_split(x, y, test_size=0.2)
    clf = LinearRegression()
    # clf = svm.SVR(kernel='poly')  # svm algorithm
    clf.fit(x_train, y_train)
    accuracy = clf.score(x_test, y_test)
    print(accuracy)


if __name__ == '__main__':
    main()