import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pickle

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import Lars
from sklearn import svm

def build_df():
    print("Lendo dados")
    df = pd.read_csv("https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv")
    df = df[df.location == "World"] # take just data grouped already (world)
    df.drop(['iso_code', 'continent', 'location'], axis=1, inplace=True)
    df = df.loc[:, ['date','new_cases']] #Just need these three columns
    df = df.reset_index(drop=True)
    print("Dados lidos")
    return df

def prepare_data(df):
    print("Preparando dados")
    # Cases will be used as input for the model
    cases = df['new_cases'].to_numpy()
    save('cases.sav', cases)

    # Build an array of days to use to plot and when the user enter with the number of days ahead to predict
    days = []
    count = 0
    for elements in cases:
      count += 1
      days.append(count)
    df['days'] = days

    days_after = 9
    size = (len(cases) , days_after)
    x = np.zeros(size)
    y = np.zeros(len(cases))

    # The idea is to use a group cases of many days to predict the number of cases of one single day
    for i in range(len(cases) - days_after):
      temp = np.zeros(days_after)
      # Take the days_after's value of elements since i, for cases
      temp[0 : days_after] = cases[i : i+ days_after]
      x[i] = temp

      y[i] = cases[i+days_after] # take the number of cases as labels


    # Drop the last n days_after of arrays because it only gets 0
    x = x[0:len(df) - days_after]
    y = y[0:len(df) - days_after]
    # Then drop the value of number days since this values aren't in the x and y anymore
    days = days[0:len(df) - days_after]

    split = int(0.67*len(x))
    days = days[split:]
    print("Dados preparados")
    return x, y, split

def build_model(df):
    print("Montando modelo")
    x, y, split = prepare_data(df)
    model = Lars(n_nonzero_coefs=1000)
    X_train, X_test, y_train, y_test = x[:split], x[split:], y[:split], y[split:]
    # X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
    model.fit(X_train, y_train)
    print("{}".format(np.linalg.norm(model.predict(X_test) - y_test, 1)/len(y_test)))
    predict = model.predict(X_test)
    cross_val_score(model, X_train, y_train, cv = 2)
    print("Modelo montado")
    return model

def save(filename, obj):
    pickle.dump(obj, open(filename, 'wb'))


df = build_df()
model = build_model(df)
save('model.sav', model)
print("FIM")
