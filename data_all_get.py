# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:12:14 2018

@author: huangjin
"""
from odps import ODPS
from odps.df import DataFrame
import pandas as pd
def data_to_local():
    # quant_financial_report_balance_sheet 资产负债表
    o = ODPS('***', '***', 'gravity_quant')
    balance_sheet = DataFrame(o.get_table('quant_financial_report_balance_sheet'))
    balance_sheet = balance_sheet.to_pandas()
    balance_sheet.to_csv('financial_report_balance_sheet.csv', index=False)
    # quant_financial_report_profitloss 利润表
    o = ODPS('***', '***', 'gravity_quant')
    profitloss_sheet = DataFrame(o.get_table('quant_financial_report_profitloss'))
    profitloss_sheet = profitloss_sheet.to_pandas()
    profitloss_sheet.to_csv('quant_financial_report_profitloss.csv', index=False)
    # quant_financial_report_cashflows_statement 现金流表
    o = ODPS('***', '***', 'gravity_quant')
    cashflows_sheet = DataFrame(o.get_table('quant_financial_report_cashflows_statement'))
    cashflows_sheet = cashflows_sheet.to_pandas()
    cashflows_sheet.to_csv('quant_financial_report_cashflows_statement.csv', index=False)
    # quant_financial_analysis_report 财务分析表
    o = ODPS('***', '***', 'gravity_quant')
    analysis_sheet = DataFrame(o.get_table('quant_financial_analysis_report'))
    analysis_sheet = analysis_sheet.to_pandas()
    analysis_sheet.to_csv('quant_financial_analysis_report.csv', index=False)
    # market_values_end 市值数据
    o = ODPS('***', '***', 'gravity_quant')
    market_value = DataFrame(o.get_table('tdl_huangjin_market_values_all'))
    market_value = market_value.to_pandas()
    print(market_value.shape)
    market_value.drop_duplicates(subset=['code', 'pt'], keep='first', inplace=True)
    market_value = market_value.dropna(subset=['code', 'pt', 'total_value'])
    market_value.to_csv('market_values_end.csv', index=False)
    # 行业信息数据
    o = ODPS('***', '***', 'gravity_quant')
    quant_stocks_industry_info = DataFrame(o.get_table('quant_stocks_industry_info'))
    quant_stocks_industry_info = quant_stocks_industry_info.to_pandas()
    a = quant_stocks_industry_info['industry_sw'].str.split('-',expand=True).add_prefix('level_')
    stocks_info = pd.concat([quant_stocks_industry_info, a], axis=1)
    stocks_info.to_csv('stocks_info.csv', index=False)
    
    
    
    
    