# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 13:12:33 2018

@author: huangjin
"""

def eval_metric(y_pred, dtrain):
    y_true = dtrain.get_label()
    res = 0
    for i in range(len(y_true)):
        res = res + min(abs(y_pred[i]/(y_true[i]+0.001) - 1), 0.8)
    res = res/len(y_true)
    return 'res', res
def eval_metric_test(y_pred, y_true):
    res = 0
    for i in range(len(y_true)):
        res = res + min(abs(y_pred[i]/(y_true[i]+0.001) - 1), 0.8)
    res = res/len(y_true)
    return res