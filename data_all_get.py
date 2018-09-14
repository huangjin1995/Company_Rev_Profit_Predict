# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 14:12:14 2018

@author: huangjin
"""
from odps import ODPS
from odps.df import DataFrame
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