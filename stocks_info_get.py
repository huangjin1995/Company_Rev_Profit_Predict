# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 14:37:32 2018

@author: huangjin
"""
from odps import ODPS
from odps.df import DataFrame
import pandas as pd
o = ODPS('***', '***', 'gravity_quant')
quant_stocks_industry_info = DataFrame(o.get_table('quant_stocks_industry_info'))
quant_stocks_industry_info = quant_stocks_industry_info.to_pandas()
a = quant_stocks_industry_info['industry_sw'].str.split('-',expand=True).add_prefix('level_')
stocks_info = pd.concat([quant_stocks_industry_info, a], axis=1)
stocks_info.to_csv('stocks_info.csv', index=False)

