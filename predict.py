import pickle
from datetime import date
import numpy as np
import sys

# load the model from disk
loaded_model = pickle.load(open('model.sav', 'rb'))
cases = pickle.load(open('cases.sav', 'rb'))

def predict(days):
    days_after = 9
    size = (2 , days_after)
    new_cases = cases
    for i in range(1, days+1):
        currentX = np.zeros(size)
        temp = np.zeros(days_after)
        temp[:days_after] = new_cases[-days_after:] # the last n days_after cases
        currentX[0] = temp
        currentX[1] = temp

        prediction = loaded_model.predict(currentX)
        prediction = prediction[0]
        new_cases = np.append(new_cases, prediction)
        print(str(i)+" -> " + str(int(prediction)))

# print(sys.argv[1])
predict(int(sys.argv[1]))
