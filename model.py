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
import math
import os
from utils import eval_metric, eval_metric_test
import datetime
starttime = datetime.datetime.now()
industry_name = ['非银金融','纺织服装','有色金属','计算机','交通运输','医药生物','钢铁','家用电器',
 '采掘','国防军工','房地产','建筑材料','休闲服务','综合','建筑装饰','银行',
 '轻工制造','化工','电子','机械设备','商业贸易','通信','电气设备','公用事业','传媒',
 '农林牧渔','食品饮料','汽车']
industry_name_english = ['Non bank finance', 'textile and clothing', 'non-ferrous metals', 
                         'computer', 'transportation', 'medical biology', 'steel', 
                         'household appliances','Excavation','Defense Force',
                         'Real Estate', 'Building Materials', 'Leisure Services', 
                         'Comprehensive', 'Architectural Decoration', 'Bank',
                         'Light manufacturing', 'Chemical', 'Electronic', 'Mechanical equipment', 
                         'Commercial trade', 'Communication', 'Electrical equipment', 'Utilities', 
                         'Media','Agriculture and fishing', 'food and beverage', 'car']
dict_result = {}
for industry_name_i in range(len(industry_name_english)):
    model_dir = './'
    test_time = '2016-03-31'
    # target = 'oper_rev'
    target = 'net_profit_is'
    industry_path = model_dir + industry_name_english[industry_name_i] +'/'+target+'/' + test_time +'/'
    train_data = pd.read_csv(industry_path + 'train.csv')
    valid_data = pd.read_csv(industry_path + 'valid.csv')
    test_data = pd.read_csv(industry_path + 'test.csv')
    test_data_real = pd.read_csv(industry_path + 'test_real.csv')
    print(train_data.shape)
    print(valid_data.shape)
    print(test_data.shape)
    print(test_data_real.shape)
    cols = [c for c in train_data.columns if c not in ['code','pt', 
                                                       target, 'stm_issuingdate', 'stm_predict_issuingdate']]
    X_train = train_data[cols]
    y_train = train_data[target]
    y_train = round(y_train/1000000,2)
    X_validate = valid_data[cols]
    y_validate = valid_data[target]
    y_validate = round(y_validate/1000000,2)
    X_test = test_data[cols]
    X_train_set = xgb.DMatrix(X_train, label=y_train, missing=np.NAN)
    X_validate_set = xgb.DMatrix(X_validate, label=y_validate, missing=np.NAN)
    X_test_set = xgb.DMatrix(X_test, missing=np.NAN)
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
    pred_y = gbm.predict(X_test_set)
    pred_y = list(pred_y)
    print(sum([int(i<0) for i in pred_y]))
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
    # 保存结果
    res = pd.Series(pred_y)
    res = res.apply(lambda x: 0 if x<0 else x)
    res.replace(0, res.mean(), inplace=True)
    pred_stock = test_data['code'].reset_index(drop=True)
    res.name = target
    result = pd.concat([pred_stock, res], axis=1)
    print(result.shape)
    print(test_data_real.shape)
    test_data_real[target] = round(test_data_real[target]/1000000,2)
    test_data_real = test_data_real.rename(columns={target:target + '_real'})
    pred_end = pd.merge(result, test_data_real[['code', target + '_real']], how='left', on=['code'])
    pred_end['eval']=abs(pred_end[target]-pred_end[target + '_real'])/pred_end[target + '_real']
    pred_end.to_csv(industry_path +'result_real_huamu.csv', index=False)
    a = list(pred_end[target])
    b = list(pred_end[target + '_real'])
    print(eval_metric_test(a, b))
    # 画结果曲线图
    plt.figure()
    plt.plot(a,"x-",label="pred")
    plt.plot(b,"+-",label="true")
    plt.savefig(industry_path + 'result.jpg')
    industry_path1 = model_dir + industry_name_english[industry_name_i] +'/'
    weights = pd.read_csv(industry_path1 + 'market_values.csv')
    res_weights = pred_end.merge(weights, on = 'code', how='left')
    c = res_weights['total_value']
    c = list(round(c/100000000,2))
    def eval_metric_test_weight(y_pred, y_true, weight):
        res = 0
        for i in range(len(y_true)):
            res = res + min(abs(y_pred[i]/(y_true[i]+0.001) - 1), 0.8) * math.log2(max(c[i], 2))
        res = res/len(y_true)
        return res
    tm_res = eval_metric_test_weight(a,b,c)
    print(tm_res)
    dict_result[industry_name_english[industry_name_i]]=tm_res
######################分析结果保存##############################
model_dir = './'
save_path = model_dir + test_time + '/' + target +'/'
isExists=os.path.exists(save_path)
if not isExists:
    os.makedirs(save_path)
res_industry = pd.Series(dict_result)
res_industry.to_csv(save_path + 'result_by_industry.csv')
plt.figure(figsize=(30,10))
res_industry.plot(kind='bar', title='result_by_industry')
plt.ylabel('score')
plt.tight_layout()
plt.savefig(save_path + 'result_by_industry.jpg')
endtime = datetime.datetime.now()
print((endtime - starttime).seconds)