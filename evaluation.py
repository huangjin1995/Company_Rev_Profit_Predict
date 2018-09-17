# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:47:18 2018

@author: huangjin
"""
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
def self_eval_metric_by_stock(y_true, y_pred, weight):
    res = []
    for i in range(len(y_true)):
        res.append(min(abs(y_pred[i]/(y_true[i]+0.001) - 1), 0.8) * math.log2(max(weight[i], 2)))
    return res
def evaluation_result(test_time, target):
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
        industry_path = model_dir + industry_name_english[industry_name_i] +'/'+target+'/' + test_time +'/'
        result = pd.read_csv(industry_path + 'result_predict.csv')
        test_data_real = pd.read_csv(industry_path + 'test_real.csv')
        test_data_real[target] = round(test_data_real[target]/1000000,2)
        test_data_real = test_data_real.rename(columns={target:target + '_real'})
        
        # 指标一：对于每只股票, abs(y_pred, y_truth)/y_truth
        pred_end = pd.merge(result, test_data_real[['code', target + '_real']], how='left', on=['code'])
        pred_end['eval_1']=abs(pred_end[target]-pred_end[target + '_real'])/pred_end[target + '_real']
        # 指标二：对于每只股票, min(y_pred/y_truth, 0.8)*log(market_value)
        a = list(pred_end[target])
        b = list(pred_end[target + '_real'])
        industry_path1 = model_dir + industry_name_english[industry_name_i] +'/'
        weights = pd.read_csv(industry_path1 + 'market_values.csv')
        res_weights = pred_end.merge(weights, on = 'code', how='left')
        c = res_weights['total_value']
        c = list(round(c/100000000,2))
        pred_end['eval_2']=self_eval_metric_by_stock(a,b,c)
        pred_end[['code','eval_1','eval_2']].to_csv(industry_path + 'eval_by_stocks.csv', index=False)
        # 指标二：每个行业的评估值取平均
        tm_res = sum(self_eval_metric_by_stock(a,b,c))/len(a)
        print(tm_res)
        dict_result[industry_name_english[industry_name_i]]=tm_res
    model_dir = './'
    save_path = model_dir + test_time + '/' + target +'/'
    isExists=os.path.exists(save_path)
    if not isExists:
        os.makedirs(save_path)
    res_industry = pd.Series(dict_result)
    res_industry.to_csv(save_path + 'eval_by_industry.csv', index=False)
    plt.figure(figsize=(30,10))
    res_industry.plot(kind='bar', title='result_by_industry')
    plt.ylabel('score')
    plt.tight_layout()
    plt.savefig(save_path + 'eval_by_industry.jpg')
        
        
        
        
        
        
        
        
        
        