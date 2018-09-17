# -*- coding: utf-8 -*-
"""
Created on Thu Sep  6 15:47:18 2018

@author: huangjin
"""
from data_all_get import data_to_local
from data_process import process_data
from data_fea_gen import gen_feature_file
from data_split import split_data
from model_train import train_model
from model_pred import pred_model
from evaluation import evaluation_result
if __name__=='__main__':
    # 读取数据到本地
    data_to_local()
    # 处理数据
    process_data()
    # 提取特征：输入值，预测目标名
    gen_feature_file('oper_rev')
    # 划分数据集
    split_data('2011-03-31', 
               '2016-12-31', 
              '2017-03-31', 
               '2017-12-31',
               '2017-12-31',
               '2018-03-31', 'oper_rev')
    # 模型训练，并保存模型
    train_model('train.csv', 'valid.csv', '2018-03-31', 'oper_rev')
    # 预测
    pred_model('2018-03-31', 'oper_rev')
    # 评估
    evaluation_result('2018-03-31', 'oper_rev')
    
        
        
        
        
        
        
        
        
        
        