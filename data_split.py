# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 13:54:45 2018

@author: huangjin
"""
import pandas as pd
import numpy as np
import os
def split_data(train_start_time, 
               train_end_time, 
               valid_start_time, 
               valid_end_time, 
               test_fea_time, 
               test_time, 
               target):
    industry_name_english = ['Non bank finance', 'textile and clothing', 'non-ferrous metals', 
                             'computer', 'transportation', 'medical biology', 'steel', 
                             'household appliances','Excavation','Defense Force',
                             'Real Estate', 'Building Materials', 'Leisure Services', 
                             'Comprehensive', 'Architectural Decoration', 'Bank',
                             'Light manufacturing', 'Chemical', 'Electronic', 'Mechanical equipment', 
                             'Commercial trade', 'Communication', 'Electrical equipment', 'Utilities', 
                             'Media','Agriculture and fishing', 'food and beverage', 'car']
    for industry_name_i in industry_name_english:
        # 把目标值按时间前移一位，相当于采用前一季度特征预测后一季度营收值，这是第一层特征
        model_dir = './'
        industry_path = model_dir + industry_name_i +'/'
        data_all_end = pd.read_csv(industry_path + 'data_all_process.csv')
        test_data_real = data_all_end[data_all_end['pt']==test_time]
        data_all_with_fea_last = pd.read_csv(industry_path + 'feature_all.csv')  
        train_data = data_all_with_fea_last[data_all_with_fea_last['pt']<=train_end_time]
        print(np.sum(data_all_with_fea_last['oper_rev'].isnull()))
        valid_data = data_all_with_fea_last[(data_all_with_fea_last['pt']>=valid_start_time)&(data_all_with_fea_last['pt']<valid_end_time)]
        print(np.sum(valid_data['oper_rev'].isnull()))
        test_data = data_all_with_fea_last[data_all_with_fea_last['pt']==test_fea_time]
        print(np.sum(test_data['oper_rev'].isnull()))
        train_data = train_data.loc[train_data['oper_rev']>0]
        valid_data = valid_data.loc[valid_data['oper_rev']>0]
        print('train_data:', train_data.shape)
        print('valid_data:', valid_data.shape)
        print('test_data:', test_data.shape)
        model_dir = './'
        save_path = model_dir + industry_name_i +'/'+target+'/' + test_time +'/'
        isExists=os.path.exists(save_path)
        if not isExists:
            os.makedirs(save_path)
        train_data.to_csv(save_path+'train.csv', index=False)
        valid_data.to_csv(save_path+'valid.csv', index=False)
        test_data.to_csv(save_path+'test.csv', index=False)
        test_data_real.to_csv(save_path + 'test_real.csv', index=False)