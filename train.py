#!/usr/bin/env python
# coding: utf-8

import pickle
from pathlib import Path

import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

import xgboost as xgb

import bentoml


SEED = 42
DATA_PATH = './data/archive.zip'
MODELS_DIR = './models'

N_JOBS = 8


def target_to_y(target):
    return np.log1p(target)

def y_to_target(y):
    return np.expm1(y)


raw_df = pd.read_csv(
    DATA_PATH,
    decimal=",",
    parse_dates=["date"],
    infer_datetime_format=True
)
raw_df.drop_duplicates(inplace=True)

features_to_drop = ['date', '% Iron Feed', 'Flotation Column 01 Air Flow', '% Iron Concentrate']
raw_df.drop(columns=features_to_drop, inplace=True)


df_full_train, df_test = train_test_split(raw_df, test_size=0.2, random_state=SEED)
df_train, df_val = train_test_split(df_full_train, test_size=0.25, random_state=SEED)

def prepare_X_y(df, target_col):
    X = df.drop(columns=target_col).values
    y = target_to_y(df[target_col].values)
    return X, y

target_col = '% Silica Concentrate'
feature_names = raw_df.columns.drop(target_col)

X_full_train, y_full_train = prepare_X_y(df_train, target_col)
X_train, y_train = prepare_X_y(df_train, target_col)
X_val, y_val = prepare_X_y(df_val, target_col)
X_test, y_test = prepare_X_y(df_test, target_col)

del df_full_train, df_train, df_val, df_test

dfulltrain = xgb.DMatrix(X_full_train, label=y_full_train)
dtest = xgb.DMatrix(X_test, label=y_test)

xgb_params = {  
    'objective': 'reg:squarederror',
    'eta': 0.3,
    'max_depth': 20,
    'min_child_weight': 2,
    'nthread': N_JOBS,
    'seed': SEED,
}

evals = [(dfulltrain, 'full_train'), (dtest, 'test')]
num_boost_round = 200

evals_result = {}
bst = xgb.train(
    params=xgb_params,
    dtrain=dfulltrain,
    num_boost_round=num_boost_round,
    evals=evals,
    early_stopping_rounds = True,
    evals_result=evals_result,
    verbose_eval=True
)
print("RMSE: {'full_train': %s , 'test': %s}" % (evals_result['full_train']['rmse'][-1], evals_result['test']['rmse'][-1]))

model = bst

# Save model as Python object
model_path = Path(MODELS_DIR) / 'model.bin'
with open(model_path, 'wb') as f_out:
    pickle.dump(model, f_out)

# Save as Bentoml model
bentoml.xgboost.save_model(
    'ore_impurity_model',
    model,
)