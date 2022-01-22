import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import pickle


df = pd.read_csv('eda_data.csv')
# print(df.columns)

# choose relevant columns
# get dummy data (using pd.get_dummies) i.e. for each category a different column
# train test split
# mutiple linear regression
# lasso regression
# random forest
# tune these models using GridSearchCV
# test ensembles

# choose relevant columns
# print(df.columns)
df_model = df[['avg_salary', 'Rating', 'Size', 'Type of ownership', 'Industry', 'Sector', 'Revenue', 'competitor_count', 'hourly', 'employer_provided', 'job_state', 'same_state', 'age', 'python_jd', 'spark_jd', 'aws_jd', 'excel_jd', 'job_simplified', 'seniority', 'jd_len']]

# get dummy data (using pd.get_dummies) i.e. for each category a different column
df_dummy = pd.get_dummies(df_model)
# print(df_dummy)


# train test split
from sklearn.model_selection import train_test_split
X = df_dummy.drop('avg_salary', axis = 1)
y = df_dummy['avg_salary'].values
# print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# print(list(X_test.iloc[1,:]))

# mutiple linear regression
import statsmodels.api as sm
X_sm = sm.add_constant(X)
model_sm = sm.OLS(y, X_sm)
# print(model_sm.fit().summary())

# LinearRegression
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score, KFold

lr = LinearRegression()
lr.fit(X_train, y_train)
# see what happens when you DON'T SHUFFLE: https://www.kaggle.com/getting-started/59719
kf = KFold(shuffle=True, n_splits=3)
scores = cross_val_score(lr, X_train, y_train, cv=kf, scoring='neg_mean_absolute_error')
print('LR mean cross_val_score: {}'.format(np.mean(scores)))

# L1 regularization using Lasso Regression
from sklearn.linear_model import Lasso
lr_l = Lasso()
kf_l = KFold(shuffle=True, n_splits=3)
scores_l = cross_val_score(lr_l, X_train, y_train, cv=kf_l, scoring='neg_mean_absolute_error')
print('Lasso LR mean cross_val_score: {}'.format(np.mean(scores_l)))

alphas = [i/10 for i in range(1,100)]
errors = []
for alpha in alphas:
    lr_l = Lasso(alpha=alpha)
    errors.append(np.mean(cross_val_score(lr_l, X_train, y_train, cv=kf_l, scoring='neg_mean_absolute_error')))

# plt.plot(alphas, errors)
df_alpha_error = pd.DataFrame({'alpha':alphas, 'error':errors})
# print alpha
alphas_efficient = df_alpha_error[df_alpha_error['error'] == max(df_alpha_error['error'])]
# print(alphas_efficient['alpha'][0])
# consider Lasso model with efficient alpha value 
# print(alphas_efficient['alpha'][0])
lr_l = Lasso(alpha=0.1)
lr_l.fit(X_train, y_train)

# random forest
from sklearn.ensemble import RandomForestRegressor
rf = RandomForestRegressor()
print('RFR mean cross_val_score: {}'.format(np.mean(cross_val_score(rf, X_train, y_train, scoring='neg_mean_absolute_error', cv=3))))

# tune models GridsearchCV
from sklearn.model_selection import GridSearchCV
parameters = {'n_estimators':range(10, 300, 10), 'criterion':('mse', 'mae'), 'max_features':('auto', 'sqrt', 'log2')}
gs = GridSearchCV(rf, parameters, scoring='neg_mean_absolute_error', cv=3)
gs.fit(X_train, y_train)

print('GridSearchCV best_score: {}, best_estimator: {}'.format(gs.best_score_, gs.best_estimator_))

# test ensembles
tpred_lr = lr.predict(X_test)
tpred_lrl = lr_l.predict(X_test)
tpred_rf = gs.best_estimator_.predict(X_test)

from sklearn.metrics import mean_absolute_error
print('MAE for test set and OLS model: {}'.format(mean_absolute_error(y_test, tpred_lr)))
print('MAE for test set and Lasso model: {}'.format(mean_absolute_error(y_test, tpred_lrl)))
print('MAE for test set and RFR model: {}'.format(mean_absolute_error(y_test, tpred_rf)))

# combine 2 models 
print('MAE for test set and Lasso, RFR combined: {}'.format(mean_absolute_error(y_test, (tpred_lrl+tpred_rf)/2)))


pickle.dump(gs.best_estimator_, open('final_ds_salary_model.pickle', 'wb'))