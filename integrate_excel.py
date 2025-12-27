import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
import os

# 設定工作目錄
os.chdir(r'C:\Users\raymo\Desktop\SCU work\智能交易')

def integrate_excel_files():
    """
    整合5個Excel檔案到一個新的Excel檔案
    每個等分創建一個工作表
    """
    
    # 檔案名稱列表
    file_names = ['OLS.xlsx', 'RF.xlsx', 'NN3.xlsx', 'NN4.xlsx', 'NN5.xlsx', 'real.xlsx']
    model_names = ['OLS', 'RF', 'NN3', 'NN4', 'NN5', 'Real']
    
    # 等分列表 (對應 Excel 的第12-24列)
    quantiles = [10, 20, 50, 110, 120, 130, 150, 180, 200, 256, 400, 512, 1051]
    
    # 檢查檔案是否存在
    print("檢查檔案...")
    for file_name in file_names:
        if not os.path.exists(file_name):
            print(f"錯誤: 找不到檔案 {file_name}")
            return
    
    print("所有檔案都存在,開始處理...")
    
    # 讀取所有檔案
    workbooks = {}
    for file_name, model_name in zip(file_names, model_names):
        print(f"讀取 {file_name}...")
        workbooks[model_name] = openpyxl.load_workbook(file_name, data_only=True)
    
    # 創建新的工作簿
    output_wb = openpyxl.Workbook()
    output_wb.remove(output_wb.active)  # 移除預設的工作表
    
    # 為每個等分創建工作表
    for quantile in quantiles:
        sheet_name = f"{quantile}等分"
        print(f"處理 {sheet_name}...")
        
        # 創建工作表
        ws = output_wb.create_sheet(sheet_name)
        
        # 找到對應的列號 (等分值在第12-24列,對應quantiles列表的索引)
        row_index = quantiles.index(quantile) + 12  # Excel的列號(從12開始)
        
        # 獲取時間標題 (從OLS檔案的第11列,從D欄開始到EL欄)
        ols_sheet = workbooks['OLS']['累積報酬']
        time_headers = ['時間']  # 第一個是"時間"
        
        # 從第4欄(D欄,2014/01)到第142欄(EL欄,2025/07)
        for col in range(4, 143):  # 4到142,包含142
            cell_value = ols_sheet.cell(row=11, column=col).value
            if cell_value:  # 確保不是空值
                time_headers.append(cell_value)
        
        # 寫入第1列: 投資組合 | 公司數 | 1051
        ws['A1'] = '投資組合'
        ws['B1'] = '公司數'
        ws['C1'] = 1051
        
        # 寫入第2列: X等分 | 時間 | 2014/01 | ...
        ws['A2'] = sheet_name
        for col_idx, header in enumerate(time_headers, start=2):
            ws.cell(row=2, column=col_idx, value=header)
        
        # 寫入模型數據 (從第3列開始)
        current_row = 3
        
        # 為每個模型寫入數據
        for model_name in model_names:
            wb = workbooks[model_name]
            sheet = wb['累積報酬']
            
            # 第一欄空白,第二欄是模型名稱
            ws.cell(row=current_row, column=1, value='')
            ws.cell(row=current_row, column=2, value=model_name)
            
            # 從第3欄開始寫入數據 (對應Excel的D欄到EL欄)
            for col_idx, excel_col in enumerate(range(4, 143), start=3):
                value = sheet.cell(row=row_index, column=excel_col).value
                ws.cell(row=current_row, column=col_idx, value=value)
            
            current_row += 1
        
        # 添加 大盤 數據 (從 OLS 檔案的「累積報酬」工作表的第25列提取)
        ws.cell(row=current_row, column=1, value='')
        ws.cell(row=current_row, column=2, value='大盤')
        
        market_sheet = workbooks['OLS']['累積報酬']
        for col_idx, excel_col in enumerate(range(4, 143), start=3):
            value = market_sheet.cell(row=25, column=excel_col).value
            ws.cell(row=current_row, column=col_idx, value=value)
        
        # 設定凍結窗格 (凍結B欄,即凍結A和B兩欄)
        ws.freeze_panes = 'C3'  # 凍結C欄左側的所有欄位(A和B),以及第3列上方的所有列
        
        # 設定所有儲存格字體大小為18
        for row in ws.iter_rows(min_row=1, max_row=current_row, min_col=1, max_col=len(time_headers)+1):
            for cell in row:
                cell.font = Font(size=18)
        
        print(f"  {sheet_name} 完成 (包含 {len(model_names)} 個模型 + 大盤)")
    
    # 儲存新的Excel檔案
    output_filename = '累積報酬比較.xlsx'
    output_wb.save(output_filename)
    print(f"\n完成! 輸出檔案: {output_filename}")
    print(f"共創建 {len(quantiles)} 個工作表")

if __name__ == "__main__":
    print("=" * 60)
    print("Excel 檔案整合程式")
    print("=" * 60)
    print("\n確保以下檔案在指定目錄:")
    print("  C:\\Users\\raymo\\Desktop\\SCU work\\智能交易")
    print("\n需要的檔案:")
    print("  - OLS.xlsx")
    print("  - RF.xlsx")
    print("  - NN3.xlsx")
    print("  - NN4.xlsx")
    print("  - NN5.xlsx")
    print("  - real.xlsx")
    print("\n開始執行...\n")
    
    integrate_excel_files()
    
    print("\n" + "=" * 60)
    print("程式執行完畢!")
    print("輸出檔案位於: C:\\Users\\raymo\\Desktop\\SCU work\\智能交易\\累積報酬比較.xlsx")
    print("=" * 60)