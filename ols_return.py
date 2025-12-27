import openpyxl
import pandas as pd
import numpy as np

""" 讀入數據 """
IC = pd.read_excel('OLS.xlsx', sheet_name="預測IC").T
IC = np.array(IC.iloc[2:,1:4])

# 讀取 bm (bm補值、下個個月報酬補值)
bm = pd.read_excel('bm.xlsx', sheet_name="bm補值").T
# 2013/12~2025/01
bm = np.array(bm.iloc[181:,:])
bm_ret = pd.read_excel('bm.xlsx', sheet_name="下個月月報酬補值").T
bm_ret = np.array(bm_ret.iloc[181:,:])

# 讀取 size (size補值、下個個月報酬補值)
size = pd.read_excel('size.xlsx', sheet_name="size補值").T
# 2013/12~2025/01
size = np.array(size.iloc[181:,:])
size_ret = pd.read_excel('size.xlsx', sheet_name="下個月月報酬補值").T
size_ret = np.array(size_ret.iloc[181:,:])

# 讀取 mom (mom補值、下個個月報酬補值)
mom = pd.read_excel('mom.xlsx', sheet_name="mom補值").T
# 2013/12~2025/01
mom = np.array(mom.iloc[169:,:])
mom_ret = pd.read_excel('mom.xlsx', sheet_name="下個月月報酬補值").T
mom_ret = np.array(mom_ret.iloc[169:,:])

""" 計算 Return """
# 讀取或建立 Excel 檔案
workbook = openpyxl.load_workbook("OLS.xlsx")  # 如果檔案不存在，請先建立
sheet = workbook["預測IC"]  # 選擇工作表

# 2013/12~2025/01
for n in range(141):
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
    group = [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]

    for r, g in zip(row, group):
        high = np.mean(c['return'].iloc[-g:])
        low = np.mean(c['return'].iloc[:g])
        ans = high - low if sel_value > 0 else low - high
        sheet.cell(row=r, column=n+3, value=ans)

# 儲存 Excel
workbook.save("OLS.xlsx")
