import pycaret
from pycaret.datasets import get_data
from pycaret.classification import *

dataset = get_data('credit')
print(dataset.dtypes)

data = dataset.sample(frac=0.95, random_state=786).reset_index(drop=True)
data_unseen = dataset.drop(data.index).reset_index(drop=True)

print('Data for Modeling: ' + str(data.shape))
print('Unseen Data For Predictions: ' + str(data_unseen.shape))
exp_clf101 = setup(data = data, target = 'default', session_id=123) 

compare_models()