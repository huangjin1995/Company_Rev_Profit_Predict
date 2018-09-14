# Company_Rev_Profit_Predict
# 运行环境说明
anaconda python3.6  
pandas  
tqdm  
numpy  
xgboost  
matplotlib  
# 股票市值获取：对于每只股票只取一个值即可
首先在odps上运行代码（见获取市值代码.sql），
然后在本地运行market_values_get.py文件，输出market_values_end.csv文件
# 股票基本信息获取
运行stocks_info_get.py文件，输出stocks_info.csv文件
# 财务报告数据（资产负债表，利润表，现金流量表）和财务分析数据获取
运行data_all_get.py文件，输出：  
financial_report_balance_sheet.csv  
quant_financial_report_cashflows_statement.csv  
quant_financial_report_profitloss.csv  
quant_financial_analysis_report.csv文件  
# 数据处理
文件名：data_process.py  
输入：股票市值表，资产负债表，利润表，现金流量表， 财务分析数据表；  
输出：每一个行业都有一个独立文件，每个文件包含data_all_process.csv和market_values.csv，分别代表该行业的全量数据（包括特征和标签），市场值数据；  
代码说明：由于财务报表和财务分析表的数据采集形式不一致，其中财务报表的数据是累计值（按年划分），财务分析表的数据是属于当季度的，因此首先需要把财务报表的数据按照不同股票代码和年份，对特征做差，提取出当季度的特征和目标值；财务分析数据不需要做差，最后得到处理后的数据；
代码里的gen_data函数实现求差值的功能
# 数据集划分
文件名：data_split.py  
输入：训练集起始时间、训练集终止时间、验证集起始时间、验证集终止时间、测试集特征时间、测试集实际时间、目标值  
输出：对于不同目标值，建立不同文件夹，每个文件夹下针对所需预测的季度，又建立不同文件夹，里面存放训练集，验证集，测试集，测试集真实数据
代码说明：首先把目标值按时间前移一位，相当于采用前一季度特征预测后一季度营收值，这是第一层特征，然后提取当前季度与上一季度的特征差值，上两季度的特征差值，由函数gen_feature完成，last_num参数可以控制具体需要几个季度的差值；同比特征由函数gen_feature_tongbi实现，这里没用到；最后把得到特征根据不同的时间段划分训练集，验证集，测试集；
# 模型训练与预测
输入：需要预测的目标值，预测的季度时间
输出：模型特征重要度表格，模型特征重要度曲线，预测结果和真实结果以及另外一个指标值（abs(ypred-ytruth)/ytruth）。每个行业的预测得分对比图和表格。
# 评价指标
utils.py文件，自定义指标

