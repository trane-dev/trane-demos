from sklearn.datasets import load_wine
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
import lightgbm as lgb
import xgboost as xgb
import warnings

from btb.tuning import Tunable
from btb.tuning import hyperparams as hp

def automl(X, y):
    models = {
        'LGB': lgb.LGBMRegressor,
        'XGB': xgb.XGBRegressor,
        'DTC': DecisionTreeRegressor,
        'SGDC': SGDRegressor,
        'RF': RandomForestRegressor,
    }

    def scoring_function(model_name, hyperparameter_values):
        model_class = models[model_name]
        model_instance = model_class(**hyperparameter_values)
        skf = StratifiedKFold(n_splits=5)
        scores = cross_val_score(
            estimator=model_instance,
            X=X,
            y=y,
            scoring=make_scorer(mean_squared_error),
            cv=skf,
            n_jobs=-1
        )
        return scores.mean()

    tunables = {
        'LGB': Tunable({
            'num_leaves': hp.IntHyperParam(min=2, max=100),
            'max_depth': hp.IntHyperParam(min=3, max=200),
            'learning_rate': hp.FloatHyperParam(min=0.01, max=1),
            'n_estimators': hp.IntHyperParam(min=10, max=1000),
        }),
        'XGB': Tunable({
            'max_depth': hp.IntHyperParam(min=3, max=200),
            'learning_rate': hp.FloatHyperParam(min=0.01, max=1),
            'n_estimators': hp.IntHyperParam(min=10, max=1000),
        }),
        'DTC': Tunable({
            'max_depth': hp.IntHyperParam(min=3, max=200),
            'min_samples_split': hp.FloatHyperParam(min=0.01, max=1)
        }),
        'SGDC': Tunable({
            'max_iter': hp.IntHyperParam(min=1, max=5000, default=1000),
            'tol': hp.FloatHyperParam(min=1e-3, max=1, default=1e-3),
        }),
        'RF': Tunable({
            'n_estimators': hp.IntHyperParam(min=10, max=1000),
            'max_depth': hp.IntHyperParam(min=3, max=200),
            'min_samples_split': hp.FloatHyperParam(min=0.01, max=1),
        }),
    }

    from btb import BTBSession

    session = BTBSession(
        tunables=tunables,
        scorer=scoring_function,
        verbose=True
    )

    best_proposal = session.run(10)

    return best_proposal