# Company_Rev_Profit_Predict
# 运行环境说明
anaconda python3.6  
pandas  
tqdm  
numpy  
xgboost  
matplotlib  
# 数据获取到本地
文件名：data_all_get.py  
功能：从ODPS上获取数据到本地 
# 数据处理
文件名：data_process.py  
输入：股票市值表，资产负债表，利润表，现金流量表， 财务分析数据表；  
输出：每一个行业都有一个独立文件，每个文件包含data_all_process.csv和market_values.csv，分别代表该行业的全量数据（包括特征和标签），市场值数据；  
代码说明：由于财务报表和财务分析表的数据采集形式不一致，其中财务报表的数据是累计值（按年划分），财务分析表的数据是属于当季度的，因此首先需要把财务报表的数据按照不同股票代码和年份，对特征做差，提取出当季度的特征和目标值；财务分析数据不需要做差，最后得到处理后的数据；
代码里的gen_data函数实现求差值的功能
# 数据特征提取
文件名：data_fea_gen.py  
输入：预测目标值  
输出：得到提取的特征文件
代码说明：首先把目标值按时间前移一位，相当于采用前一季度特征预测后一季度营收值，这是第一层特征，然后提取当前季度与上一季度的特征差值，上两季度的特征差值，由函数gen_feature完成，last_num参数可以控制具体需要几个季度的差值；同比特征由函数gen_feature_tongbi实现，这里没用到；
# 数据集划分
文件名：data_split.py  
输入： 时间起始点和预测目标值  
输出：训练集，验证集，测试集  
# 模型训练
文件名：model_train.py  
输入：训练集数据，验证集数据，预测目标值  
输出：模型特征重要度表格，模型特征重要度曲线等  
# 模型预测
文件名：model_pred.py  
输入：预测时间段， 预测目标值  
输出： 预测结果  
# 评估
文件名：evaluation.py  
输入：预测时间段， 预测目标值  
输出1：每个股票的评估值， 包括两个指标  
输出2：每个行业的评估指标统计  
# 评价函数
指标一：abs(y_pred, y_truth)/y_truth  
指标二：  min(y_pred/y_truth, 0.8)*log(market_value)  
# 运行文件
文件名： demo.py  


