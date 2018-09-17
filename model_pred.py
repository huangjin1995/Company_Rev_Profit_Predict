# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:47:18 2018

@author: huangjin
"""
import pandas as pd
import numpy as np
import xgboost as xgb
import os
def pred_model(test_time, target):
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
        industry_path = model_dir + industry_name_english[industry_name_i] +'/'+target+'/' + test_time +'/'
        test_data = pd.read_csv(industry_path + 'test.csv')
        cols = [c for c in test_data.columns if c not in ['code','pt', 
                                                           target, 'stm_issuingdate', 'stm_predict_issuingdate']]
        X_test = test_data[cols]
        X_test_set = xgb.DMatrix(X_test, missing=np.NAN)
        gbm = xgb.Booster(model_file=industry_path + 'xgboost.model')
        pred_y = gbm.predict(X_test_set)
        pred_y = list(pred_y)
        # 保存结果
        res = pd.Series(pred_y)
        res = res.apply(lambda x: 0 if x<0 else x)
        res.replace(0, res.mean(), inplace=True)
        pred_stock = test_data['code'].reset_index(drop=True)
        res.name = target
        result = pd.concat([pred_stock, res], axis=1)
        print(result.shape)
        result.to_csv(industry_path + 'result_predict.csv', index=False)