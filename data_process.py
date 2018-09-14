# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 15:51:36 2018

@author: huangjin
"""
import pandas as pd
from tqdm import tqdm
import os
def gen_data(df, time_start, time_end):
    df = df.sort_values(by=['code','pt'])
    df = df[(df['pt']<=time_end)&(df['pt']>=time_start)]
    col = [c for c in df.columns if c not in ['code','pt']]
    df_tem = df.groupby(['code']).shift(1).fillna(0)
    all_data = df[['code','pt']]
    for j in tqdm(range(len(col))):
        tem = df[col[j]]-df_tem[col[j]]
        all_data = pd.concat([all_data, tem], axis=1)
    return all_data
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
for industry_name_i in range(len(industry_name)):
    # 市场值
    market_value = pd.read_csv('market_values_end.csv')
    stocks_info = pd.read_csv('stocks_info.csv')
    stock_info_tem = stocks_info[['code','level_0']]
    stock_info_tem = stock_info_tem[stock_info_tem['level_0']==industry_name[industry_name_i]]
    market_values = pd.merge(stock_info_tem, market_value, how='left', on = 'code')
    market_values.drop('level_0', axis=1, inplace=True)
    # 资产负债表
    data_all = pd.read_csv('financial_report_balance_sheet.csv')
    stocks_info = pd.read_csv('stocks_info.csv')
    stock_info_tem = stocks_info[['code','level_0']]
    stock_info_tem = stock_info_tem[stock_info_tem['level_0']==industry_name[industry_name_i]]
    balance_data = pd.merge(stock_info_tem, data_all, how='left', on = 'code')
    balance_data.drop('level_0', axis=1, inplace=True)
    print(balance_data.shape)
    # 利润表
    data_all = pd.read_csv('quant_financial_report_profitloss.csv')
    stocks_info = pd.read_csv('stocks_info.csv')
    stock_info_tem = stocks_info[['code','level_0']]
    stock_info_tem = stock_info_tem[stock_info_tem['level_0']==industry_name[industry_name_i]]
    income_data = pd.merge(stock_info_tem, data_all, how='left', on = 'code')
    income_data.drop('level_0', axis=1, inplace=True)
    print(income_data.shape)
    # 现金流量表
    data_all = pd.read_csv('quant_financial_report_cashflows_statement.csv')
    stocks_info = pd.read_csv('stocks_info.csv')
    stock_info_tem = stocks_info[['code','level_0']]
    stock_info_tem = stock_info_tem[stock_info_tem['level_0']==industry_name[industry_name_i]]
    flow_data = pd.merge(stock_info_tem, data_all, how='left', on = 'code')
    flow_data.drop('level_0', axis=1, inplace=True)
    print(flow_data.shape)
    tem1 = pd.merge(income_data, balance_data, on=['code','pt'], how = 'left')
    data_all = pd.merge(tem1, flow_data, on=['code','pt'], how = 'left')
    thresh = 0.8*len(data_all)
    print('去除缺失值前的维度:', data_all.shape)
    data_all.dropna(axis=1, thresh=thresh, inplace=True)
    print('去除缺失值后的维度:', data_all.shape)
    # 去除和目标值重复的列tot_oper_rev
    data_all.drop('tot_oper_rev', axis=1, inplace=True)
    # 前驱值填充
    data_all = data_all.fillna(method='ffill')
    # 没有前驱值，中值填充
    data_all = data_all.fillna(data_all.median())
    # '2011-03-31'， '2018-03-31'
    print(data_all.shape)
    # 对data_all按照code对相邻时间做差，因为原始特征都是累加的
    data1 = gen_data(data_all, '2011-03-31', '2011-12-31')
    data2 = gen_data(data_all, '2012-03-31', '2012-12-31')
    data3 = gen_data(data_all, '2013-03-31', '2013-12-31')
    data4 = gen_data(data_all, '2014-03-31', '2014-12-31')
    data5 = gen_data(data_all, '2015-03-31', '2015-12-31')
    data6 = gen_data(data_all, '2016-03-31', '2016-12-31')
    data7 = gen_data(data_all, '2017-03-31', '2017-12-31')
    data8 = gen_data(data_all, '2018-03-31', '2018-12-31')
    data_all_end = pd.DataFrame()
    data_all_end = data_all_end.append(data1)
    data_all_end = data_all_end.append(data2)
    data_all_end = data_all_end.append(data3)
    data_all_end = data_all_end.append(data4)
    data_all_end = data_all_end.append(data5)
    data_all_end = data_all_end.append(data6)
    data_all_end = data_all_end.append(data7)
    data_all_end = data_all_end.append(data8)
    print(data_all_end.shape)
    # 财务分析数据表
    data_all = pd.read_csv('quant_financial_analysis_report.csv')
    stocks_info = pd.read_csv('stocks_info.csv')
    stock_info_tem = stocks_info[['code','level_0']]
    stock_info_tem = stock_info_tem[stock_info_tem['level_0']==industry_name[industry_name_i]]
    fin_data = pd.merge(stock_info_tem, data_all, how='left', on = 'code')
    fin_data.drop('level_0', axis=1, inplace=True)
    thresh = 0.8*len(fin_data)
    print('去除缺失值前的维度:', fin_data.shape)
    fin_data.dropna(axis=1, thresh=thresh, inplace=True)
    print('去除缺失值后的维度:', fin_data.shape)
    # 前驱值填充
    fin_data = fin_data.fillna(method='ffill')
    # 没有前驱值，中值填充
    fin_data = fin_data.fillna(data_all.median())
    print(fin_data.shape)
    data_all_end = pd.merge(data_all_end, fin_data, on=['code','pt'], how = 'left')
    data_all_end = data_all_end.sort_values(by=['code','pt'])
    model_dir = './'
    industry_path = model_dir + industry_name_english[industry_name_i] +'/'
    os.makedirs(industry_path)
    data_all_end.to_csv(industry_path + 'data_all_process.csv', index=False)
    market_values.to_csv(industry_path + 'market_values.csv', index=False)    