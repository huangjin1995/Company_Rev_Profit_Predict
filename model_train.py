# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:47:18 2018

@author: huangjin
"""
import pandas as pd
import numpy as np
import xgboost as xgb
import matplotlib.pyplot as plt
import operator
def eval_metric(y_pred, dtrain):
    y_true = dtrain.get_label()
    res = 0
    for i in range(len(y_true)):
        res = res + min(abs(y_pred[i]/(y_true[i]+0.001) - 1), 0.8)
    res = res/len(y_true)
    return 'res', res
def train_model(train_file, valid_file, test_time, target):
    industry_name_english = ['Non bank finance', 'textile and clothing', 'non-ferrous metals', 
                             'computer', 'transportation', 'medical biology', 'steel', 
                             'household appliances','Excavation','Defense Force',
                             'Real Estate', 'Building Materials', 'Leisure Services', 
                             'Comprehensive', 'Architectural Decoration', 'Bank',
                             'Light manufacturing', 'Chemical', 'Electronic', 'Mechanical equipment', 
                             'Commercial trade', 'Communication', 'Electrical equipment', 'Utilities', 
                             'Media','Agriculture and fishing', 'food and beverage', 'car']
    for industry_name_i in range(len(industry_name_english)):
        model_dir = './'
        # test_time = '2016-03-31'
        # target = 'oper_rev'
        industry_path = model_dir + industry_name_english[industry_name_i] +'/'+target+'/' + test_time +'/'
        train_data = pd.read_csv(industry_path + train_file)
        valid_data = pd.read_csv(industry_path + valid_file)
        print(train_data.shape)
        print(valid_data.shape)
        cols = [c for c in train_data.columns if c not in ['code','pt', 
                                                           target, 'stm_issuingdate', 'stm_predict_issuingdate']]
        X_train = train_data[cols]
        y_train = train_data[target]
        y_train = round(y_train/1000000,2)
        X_validate = valid_data[cols]
        y_validate = valid_data[target]
        y_validate = round(y_validate/1000000,2)
        X_train_set = xgb.DMatrix(X_train, label=y_train, missing=np.NAN)
        X_validate_set = xgb.DMatrix(X_validate, label=y_validate, missing=np.NAN)
        watchlist = [(X_train_set, 'train'),(X_validate_set, 'valid')]
        params = {"objective": "reg:linear",
                   "eta": 0.05,  # 0.15
                   "max_depth": 10,
                   "subsample": 0.7,
                   "colsample_bytree": 0.7,
                   "silent": 1,
                   }
        gbm = xgb.train(params, X_train_set, num_boost_round=2000, evals=watchlist,\
                        feval = eval_metric, early_stopping_rounds=50, maximize=False, verbose_eval=100)
        gbm.save_model(industry_path + 'xgboost.model')
        # 保存模型重要度文件
        importance = gbm.get_fscore()
        importance = sorted(importance.items(), key=operator.itemgetter(1))
        df = pd.DataFrame(importance, columns=['feature', 'fscore'])
        df['fscore'] = df['fscore'] / df['fscore'].sum()
        df.to_csv(industry_path + 'model_feature_importance.csv', index=False)
        # 保存模型重要度图片
        feat_imp = pd.Series(gbm.get_fscore()).sort_values(ascending=False)
        plt.figure(figsize=(30,10))
        feat_imp.plot(kind='bar', title='Feature Importances')
        plt.ylabel('Feature Importance Score')
        plt.savefig(industry_path + 'feat_importance.jpg')