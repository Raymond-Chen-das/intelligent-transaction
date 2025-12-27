# 引入需要的套件
import os
import pandas as pd
import numpy as np
import openpyxl

# 定義路徑
os.chdir(r'C:\Users\raymo\Desktop\SCU work\智能交易')

# 讀取 Excel 檔案
workbook = openpyxl.load_workbook("real.xlsx")  # 如果檔案不存在，請先建立
sheet = workbook["真實IC"]  # 選擇工作表

# 讀入數據
IC = pd.read_excel('real.xlsx', sheet_name="真實IC").T
IC = np.array(IC.iloc[2:, 1:4])

# 讀取 bm（bm補值、下個月月報酬補值）
bm = pd.read_excel('bm.xlsx', sheet_name="bm補值").T
# 2013/12~2025/01  2013/12-2025/07
bm = np.array(bm.iloc[181:, :])
bm_ret = pd.read_excel('bm.xlsx', sheet_name="下個月月報酬補值").T
bm_ret = np.array(bm_ret.iloc[181:, :])

# 讀取 size（size補值、下個月月報酬補值）
size = pd.read_excel('size.xlsx', sheet_name="size補值").T
# 2013/12~2025/01  2013/12-2025/07
size = np.array(size.iloc[181:, :])
size_ret = pd.read_excel('size.xlsx', sheet_name="下個月月報酬補值").T
size_ret = np.array(size_ret.iloc[181:, :])

# 讀取 mom（mom補值、下個月月報酬補值）
mom = pd.read_excel('mom.xlsx', sheet_name="mom補值").T
# 2013/12~2025/01  2013/12-2025/07
mom = np.array(mom.iloc[169:, :])
mom_ret = pd.read_excel('mom.xlsx', sheet_name="下個月月報酬補值").T
mom_ret = np.array(mom_ret.iloc[169:, :])

# 讀取 ID
ID = pd.read_excel('bm.xlsx', sheet_name="bm補值")
ID = np.array(ID.iloc[:, 0:2])

# 計算投資組合
# 2013/12~2025/01  2013/12-2025/07
for n in range(140):  # 根據註解調整為 140
    c = pd.DataFrame()
    sel_index = np.argmax(abs(IC[n]))
    sel_value = IC[n][sel_index]
    
    # 選擇因子與報酬
    if sel_index == 0:
        fac, sel, ret = bm[n], 'bm', bm_ret[n]
    elif sel_index == 1:
        fac, sel, ret = size[n], 'size', size_ret[n]
    elif sel_index == 2:
        fac, sel, ret = mom[n], 'mom', mom_ret[n]
    
    c['factor'] = fac
    c['return'] = ret
    c['rank'] = c['factor'].rank(method='max')
    c = c.sort_values(by='rank')
    
    row = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
    group = [105, 53, 21, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    for r, g in zip(row, group):
        high = np.mean(c['return'].iloc[-g:])
        low = np.mean(c['return'].iloc[:g])
        ans = high - low if sel_value > 0 else low - high
        sheet.cell(row=r, column=n+3, value=ans)

# 存檔
workbook.save("real.xlsx")