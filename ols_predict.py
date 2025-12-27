"""使用說明

記得要改參數!!!
(1)改路徑
(2)改Excel檔案名稱(bm size mom)
(3)改工作表名稱(bm size mom)
(4)n1, n2 = 178, 319 (如果是mom的話n1=178-12=166)
(5)改sheet.cell(row=3或4或5)

"""

"""=== Step1 引入需要的套件 ==="""
import os
import pandas as pd
import openpyxl
from sklearn.linear_model import LinearRegression

# 需要裝os、pandas、scikit-learn套件
# pip install os
# pip install scikit-learn
# pip install pandas

"""=== Step2 定義路徑 ==="""
# 設定放資料的文件夾路徑並變為當前工作目錄
# 需改成你資料存在的文件夾之路徑
os.chdir(r'C:\Users\raymo\Desktop\SCU work\智能交易')

"""=== Step3 讀入數據 ==="""
# 讀取 size補值 (x)
df_x = pd.read_excel('size.xlsx', sheet_name="size補值")  # 工作表名稱要與你的Excel檔案相同
# 讀取 sizeIC值 (y)
df_y = pd.read_excel('size.xlsx', sheet_name="sizeIC")    # 工作表名稱要與你的Excel檔案相同

"""=== Step4 數據處理 ==="""
# 轉置 (將橫列列為列成直列)
df_x = df_x.T
df_y = df_y.T

# 設定 bm補值的行標為第1列 (股票代號)
df_x.columns = df_x.iloc[0, :]
# 給定 bmIC值的行標為第1列
df_y.columns = df_y.iloc[0, :]

# 留下 1999/1 ～ 2025/1 的數據 (bm) → 刪除代號、名稱
df_x = df_x.iloc[2:, :]

# 留下 1999/1 ～ 2025/1 的數據 (IC) → 刪除Time、IC
df_y = df_y.iloc[2:, :]

"""=== Step5 劃分訓練集 ==="""
# X值 (1999/1 ～ 2013/10 的 bm值)
X = df_x.iloc[:166, :].values
# y值 (1999/1 ～ 2013/11 的 IC值)
Y = df_y.iloc[1:167, :].values

"""=== Step6 劃分測試集 ==="""
# 測試 (2013/11 的 bm值)
test_X = df_x.iloc[166:167, :].values

"""=== Step7 建立模型及預測 ==="""
# 線性迴歸
reg = LinearRegression()

# 訓練X,Y
reg.fit(X, Y)

# 顯示預測結果
print('Size')
print('=============================')
print('線性迴歸', reg.predict(test_X))


# bm
n1, n2 = 178, 319 #固定n2-n1相減為141

# 讀取或建立 Excel 檔案
workbook = openpyxl.load_workbook("OLS.xlsx")  # 如果檔案不存在，請先建立
sheet = workbook["預測IC"]  # 選擇工作表

for n in range(n1, n2):
    X = df_x.iloc[0:n, :].values
    Y = df_y.iloc[1:n+1, :].values
    test_X = df_x.iloc[n:n+1, :].values
    reg.fit(X, Y)
    predIC = reg.predict(test_X)
    # 填入工作表（預測IC）從 C3 到 EF3
    sheet.cell(row=4, column=n-n1+3, value=predIC[0,0])

# 存檔
workbook.save("OLS.xlsx")