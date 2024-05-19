from bayes_opt import BayesianOptimization
import pandas as pd
import lightgbm
import scipy
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from bayes_opt import UtilityFunction
from sklearn.linear_model import LinearRegression
import time

SUBFOLDER = "salmon_data"
PHENOTYPE = "gutted.weight.kg"

best_features = pd.read_csv(f"../../data/{SUBFOLDER}/best_features_1.csv", index_col=0)
list_best_features = list(best_features["features"].values)

XY_dataset = pd.read_csv(f"../../data/{SUBFOLDER}/transcriptome_XY.csv", index_col=0)

# One iteration
# 50 times
    # Choose 10 features
    # Train test split
    # Predict label

lgb_param_space = {
    "learning_rate": (0.001, 0.5),  
    "n_estimators": (5, 1000),
    "max_depth": (3, 16),
    "min_child_samples": (5, 300),
    "subsample": (0.5, 1),  
    "reg_alpha": (0.01, 7),
    "reg_lambda": (0, 10)
}

def regression_run(learning_rate, n_estimators, max_depth, min_child_samples, subsample, reg_alpha, reg_lambda):
    """Function with unknown internals we wish to maximize.

    One iteration
    20 times
        Choose one of the datasets
        Choose 10 features
        Train test split
        Predict label
    """
    scores = []
    for i in range(20):
        chosen_features = random.sample(list_best_features, 10)
        y = XY_dataset[PHENOTYPE]
        X = XY_dataset.drop(PHENOTYPE, axis=1)
        X = X[chosen_features]
        #print(X.shape)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        model = lightgbm.LGBMRegressor(learning_rate=learning_rate, 
                                       n_estimators=int(n_estimators),
                                       max_depth=int(max_depth),
                                       min_child_samples=int(min_child_samples),
                                       subsample=subsample,
                                       reg_alpha=reg_alpha, 
                                       reg_lambda=reg_lambda,
                                       verbose=-1)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        scores.append(mae)
    return -np.mean(scores)

optimizer = BayesianOptimization(
    f=regression_run,
    pbounds=lgb_param_space,
    verbose=2, # verbose = 1 prints only when a maximum is observed, verbose = 0 is silent
    random_state=1,
)

optimizer.maximize(
    init_points=2,
    n_iter=3,
)

utility = UtilityFunction(kind="ucb", kappa=2.5, xi=0.0)
next_point_to_probe = optimizer.suggest(utility)
target = regression_run(**next_point_to_probe)

elapsed_time = 0
while elapsed_time < 10:
    start_time = time.time()

    next_point = optimizer.suggest(utility)
    target = regression_run(**next_point)
    optimizer.register(params=next_point, target=target)

    end_time = time.time()
    elapsed_time = (end_time - start_time)/60 # minutes

    print(target, next_point)
print(optimizer.max)