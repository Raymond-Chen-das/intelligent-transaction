# 引入需要的套件
import os
import pandas as pd
import numpy as np
import openpyxl
from shutil import copy

# 定義路徑
os.chdir(r'C:\Users\raymo\Desktop\SCU work\智能交易')

# 讀取因子數據（所有模型共用）
# 讀取 bm（bm補值、下個月月報酬補值）
bm = pd.read_excel('bm.xlsx', sheet_name="bm補值").T
bm = np.array(bm.iloc[181:, :])
bm_ret = pd.read_excel('bm.xlsx', sheet_name="下個月月報酬補值").T
bm_ret = np.array(bm_ret.iloc[181:, :])

# 讀取 size（size補值、下個月月報酬補值）
size = pd.read_excel('size.xlsx', sheet_name="size補值").T
size = np.array(size.iloc[181:, :])
size_ret = pd.read_excel('size.xlsx', sheet_name="下個月月報酬補值").T
size_ret = np.array(size_ret.iloc[181:, :])

# 讀取 mom（mom補值、下個月月報酬補值）
mom = pd.read_excel('mom.xlsx', sheet_name="mom補值").T
mom = np.array(mom.iloc[169:, :])
mom_ret = pd.read_excel('mom.xlsx', sheet_name="下個月月報酬補值").T
mom_ret = np.array(mom_ret.iloc[169:, :])


def process_weighted_portfolio(input_file, output_file, sheet_name, n_range, group):
    """
    處理加權因子投資組合

    參數:
    - input_file: 輸入檔案名稱
    - output_file: 輸出檔案名稱
    - sheet_name: 要修改的工作表名稱（「真實IC」或「預測IC」）
    - n_range: 計算的時間範圍
    - group: 投資組合分組設定
    """
    print(f"處理 {input_file} -> {output_file}")

    # 複製原始檔案
    copy(input_file, output_file)

    # 讀取 IC 數據
    IC = pd.read_excel(input_file, sheet_name=sheet_name).T
    IC = np.array(IC.iloc[2:, 1:4])

    # 開啟輸出檔案
    workbook = openpyxl.load_workbook(output_file)
    sheet = workbook[sheet_name]

    # 計算投資組合（使用加權因子）
    for n in range(n_range):
        c = pd.DataFrame()

        # 加權因子：fac = bm[n] * IC[n][0] + size[n] * IC[n][1] + mom[n] * IC[n][2]
        fac = bm[n] * IC[n][0] + size[n] * IC[n][1] + mom[n] * IC[n][2]

        # 報酬率使用 bm_ret（因為三個報酬率都一樣）
        ret = bm_ret[n]

        c['factor'] = fac
        c['return'] = ret
        c['rank'] = c['factor'].rank(method='max')
        c = c.sort_values(by='rank')

        row = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

        for r, g in zip(row, group):
            high = np.mean(c['return'].iloc[-g:])
            low = np.mean(c['return'].iloc[:g])
            ans = high - low  # 固定為 high - low
            sheet.cell(row=r, column=n+3, value=ans)

    # 存檔
    workbook.save(output_file)
    print(f"完成 {output_file}")


# 定義所有要處理的模型
models = [
    {
        'input': 'real.xlsx',
        'output': 'real_weighted.xlsx',
        'sheet': '真實IC',
        'range': 140,
        'group': [105, 53, 21, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'OLS.xlsx',
        'output': 'OLS_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'RF.xlsx',
        'output': 'RF_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'NN3.xlsx',
        'output': 'NN3_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'NN4.xlsx',
        'output': 'NN4_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'NN5.xlsx',
        'output': 'NN5_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    },
    {
        'input': 'XGBoost.xlsx',
        'output': 'XGBoost_weighted.xlsx',
        'sheet': '預測IC',
        'range': 141,
        'group': [96, 48, 19, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    }
]

# 執行所有模型的處理
print("開始處理加權因子投資組合...")
for model in models:
    process_weighted_portfolio(
        input_file=model['input'],
        output_file=model['output'],
        sheet_name=model['sheet'],
        n_range=model['range'],
        group=model['group']
    )

print("\n所有檔案處理完成！")
print("已產生以下檔案：")
for model in models:
    print(f"  - {model['output']}")
