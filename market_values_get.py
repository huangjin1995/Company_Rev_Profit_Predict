# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 15:02:35 2018

@author: huangjin
"""
from odps import ODPS
from odps.df import DataFrame
import pandas as pd
o = ODPS('***', '***', 'gravity_quant')
market_value = DataFrame(o.get_table('tdl_huangjin_market_values_all'))
market_value = market_value.to_pandas()
print(market_value.shape)
market_value.to_csv('market_values.csv', index=False)

# 去重
market_value = pd.read_csv('market_values.csv')
market_value.drop_duplicates(subset=['code', 'pt'], keep='first', inplace=True)
market_value = market_value.dropna(subset=['code', 'pt', 'total_value'])
market_value.to_csv('market_values_end.csv', index=False)
