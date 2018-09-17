# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 13:54:45 2018

@author: huangjin
"""
import pandas as pd
from tqdm import tqdm
def gen_feature(df, feature_name, last_num, target_to_pred):
    df = df.sort_values(by=['code','pt'])
    col = [c for c in df.columns if c not in ['code','pt', target_to_pred, 'stm_issuingdate', 'stm_predict_issuingdate']]
    df_tem = df.groupby(['code']).shift(last_num).fillna(-1)
    all_data = df[['code','pt']]
    for j in tqdm(range(len(col))):
        tem = df[col[j]]-df_tem[col[j]]
        tem.name = col[j]+feature_name
        all_data = pd.concat([all_data, tem], axis=1)
    return all_data
def gen_feature_tongbi(df, feature_name, num_move):
    df = df.sort_values(by=['code','pt'])
    num = list(set(df['code'].values))
    lens = len(num)
    col = [c for c in df.columns if c not in ['code','pt', 'oper_rev', 'stm_issuingdate', 'stm_predict_issuingdate']]
    all_data = pd.DataFrame()
    for i in tqdm(range(lens)):
        tem_data_1 = pd.DataFrame()
        tem_data_2 = pd.DataFrame()
        for j in col:
            a = df[df['code']==num[i]]
            b = a[j].shift(num_move)
            b = b.fillna(-1)
            b.name = j+feature_name
            tem_data_1 = pd.concat([tem_data_1, b], axis=1)
        d = df[df['code']==num[i]]
        tem_data_2 = pd.concat([d[['code', 'pt']], tem_data_1], axis=1)
        all_data = all_data.append(tem_data_2)
    return all_data[['code', 'pt', 'oper_rev_fea_1'+feature_name]]
def gen_feature_file(target):
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
        # test_data_real = data_all_end[data_all_end['pt']==test_time]
        num = list(set(data_all_end['code'].values))
        lens = len(num)
        data_all = pd.DataFrame()
        for i in tqdm(range(lens)):
            a = data_all_end[data_all_end['code']==num[i]]
            b = a[target].shift(-1)
            d = a[target]
            d.name = target + '_fea_1'
            a.drop(target, axis=1, inplace=True)
            c = pd.concat([a, d, b], axis=1)
            data_all = data_all.append(c)
        print(data_all.shape)
        # 提取当前季度与上一季度的特征差值，上两季度的特征差值
        data_fea_last_1 = gen_feature(data_all, '_last_1', 1, target)
        data_fea_last_2 = gen_feature(data_all, '_last_2', 2, target)
        print(data_fea_last_1.shape)
        print(data_fea_last_2.shape)
        data_all_with_fea_last = pd.merge(data_all, data_fea_last_1, how='left', on=['code','pt'])
        data_all_with_fea_last = pd.merge(data_all_with_fea_last, data_fea_last_2, how='left', on=['code','pt'])
        print(data_all_with_fea_last.shape)
          
        # 同比特征，这里没采用
        # 3,7,11移动
        #data_fea_tongbi = gen_feature_tongbi(data_all, '_tongbi', 3)
        #print(data_fea_tongbi.shape)
        #data_all_with_fea_last = pd.merge(data_all_with_fea_last, data_fea_tongbi, how='left', on=['code','pt'])
        
        data_all_with_fea_last.to_csv(industry_path + 'feature_all.csv', index=False)
        
#        train_data = data_all_with_fea_last[data_all_with_fea_last['pt']<=train_end_time]
#        print(np.sum(data_all_with_fea_last['oper_rev'].isnull()))
#        valid_data = data_all_with_fea_last[(data_all_with_fea_last['pt']>=valid_start_time)&(data_all_with_fea_last['pt']<valid_end_time)]
#        print(np.sum(valid_data['oper_rev'].isnull()))
#        test_data = data_all_with_fea_last[data_all_with_fea_last['pt']==test_fea_time]
#        print(np.sum(test_data['oper_rev'].isnull()))
#        train_data = train_data.loc[train_data['oper_rev']>0]
#        valid_data = valid_data.loc[valid_data['oper_rev']>0]
#        print('train_data:', train_data.shape)
#        print('valid_data:', valid_data.shape)
#        print('test_data:', test_data.shape)
#        model_dir = './'
#        save_path = model_dir + industry_name_i +'/'+target+'/' + test_time +'/'
#        isExists=os.path.exists(save_path)
#        if not isExists:
#            os.makedirs(save_path)
#        train_data.to_csv(save_path+'train.csv', index=False)
#        valid_data.to_csv(save_path+'valid.csv', index=False)
#        test_data.to_csv(save_path+'test.csv', index=False)
#        test_data_real.to_csv(save_path + 'test_real.csv', index=False)