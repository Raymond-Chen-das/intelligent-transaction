# 智能交易系統 (Intelligent Trading System)

基於機器學習的台灣股票市場智能交易系統，使用多種 ML 模型預測股票因子的資訊係數（IC），並根據預測結果構建動態投資組合策略。

## 專案概述

本專案實現了完整的量化投資研究流程，從資料處理、模型訓練、預測到績效評估。核心策略是使用機器學習模型預測三個股票因子（帳面市值比、公司規模、動量）的未來資訊係數，並根據預測結果動態選擇最佳因子構建多空投資組合。

## 主要功能

- **真實 IC 基準**：使用真實 IC 值構建投資組合作為基準（real.xlsx）
- **多因子預測**：使用機器學習模型預測 bm（帳面市值比）、size（公司規模）、mom（動量）三個因子的 IC 值
- **動態因子選擇**：每期自動選擇 IC 絕對值最大的因子（真實或預測）
- **投資組合構建**：基於因子排名建立多空投資組合（13 種分組方式）
- **模型比較**：比較機器學習預測模型與真實 IC 基準的績效
- **績效評估**：計算累積報酬並與大盤比較

## 專案結構

### 核心檔案

#### 基準投資組合計算（真實 IC）
- **[portfolio.py](portfolio.py)**：使用真實 IC 值構建多因子動態投資組合，作為模型預測的基準對照（輸出 real.xlsx）
- **[single.py](single.py)**：使用真實 IC 值分析單一因子策略（非主要程式，用於額外分析）

#### 機器學習模型（IC 預測）
- **[ols_predict.py](ols_predict.py)**：線性迴歸模型預測（需手動修改參數分別預測 bm/size/mom）
- **[rf_predict.py](rf_predict.py)**：隨機森林模型預測（一次預測三個因子）
- **[nn_predict.py](nn_predict.py)**：深度神經網路模型預測（一次預測三個因子）
- **[xgboost_predict.py](xgboost_predict.py)**：XGBoost 模型預測（一次預測三個因子）

#### 投資組合報酬計算
- **[ols_return.py](ols_return.py)**：根據 OLS 預測 IC 構建投資組合並計算報酬
- **[rf_return.py](rf_return.py)**：根據隨機森林預測 IC 構建投資組合並計算報酬
- **[nn_return.py](nn_return.py)**：根據神經網路預測 IC 構建投資組合並計算報酬
- **[xgboost_return.py](xgboost_return.py)**：根據 XGBoost 預測 IC 構建投資組合並計算報酬

#### 分析工具
- **[portfolio_analysis.py](portfolio_analysis.py)**：批次處理多個模型的投資組合分析（計算 13 種分組規模的報酬）
- **[integrate_excel.py](integrate_excel.py)**：整合多個模型結果到單一 Excel 檔案（累積報酬比較）
- **[create_confusion_matrix.py](create_confusion_matrix.py)**：創建混淆矩陣工作表（計算 Accuracy、Precision、Recall、F1-score）

### 資料檔案

#### 因子資料
- **bm.xlsx**：帳面市值比因子
- **size.xlsx**：公司規模因子
- **mom.xlsx**：動量因子

#### 模型結果
- **real.xlsx**：基於真實 IC 的投資組合結果（基準）
- **OLS.xlsx**：線性迴歸模型結果
- **RF.xlsx**：隨機森林模型結果
- **NN3.xlsx**：神經網路模型結果
- **XGBoost.xlsx**：XGBoost 模型結果

#### 分析結果
- **累積報酬比較.xlsx**：整合所有模型的累積報酬比較

## 技術架構

### 機器學習模型

1. **線性迴歸 (OLS)**
   - 使用 `sklearn.linear_model.LinearRegression`
   - 預測單一因子 IC（需手動修改參數預測不同因子）
   - 基準模型，提供線性預測能力

2. **隨機森林 (Random Forest)**
   - 使用 `sklearn.ensemble.RandomForestRegressor`
   - 參數：`max_depth=3, n_estimators=100, random_state=999`
   - 一次預測三個因子 IC（bm, size, mom）
   - 捕捉非線性關係

3. **深度神經網路 (Neural Network)**
   - 使用 TensorFlow/Keras
   - 架構：5 層全連接網路 (32→16→8→1)
   - L1 正則化（1e-4）防止過擬合
   - 早停機制（patience=5，監控驗證損失）
   - 驗證集：固定 4 年（48 個月）
   - 一次預測三個因子 IC

4. **XGBoost**
   - 使用 `xgboost.XGBRegressor`
   - 參數：`n_estimators=100, max_depth=3, learning_rate=0.05`
   - 一次預測三個因子 IC
   - 梯度提升樹模型

### 投資策略流程

1. **訓練階段**：使用歷史資料（1999/01 起）滾動訓練模型
2. **預測階段**：預測下期三個因子的 IC 值（bm、size、mom）
3. **因子選擇**：選擇預測 IC 絕對值最大的因子
4. **股票排名**：根據選定因子對所有股票進行排名
5. **組合構建**：
   - 13 種分組規模：從 10 等分到 1051 等分
   - 做多排名最高的 g 支股票
   - 做空排名最低的 g 支股票
   - 根據 IC 符號決定方向（IC>0: 高減低，IC<0: 低減高）
6. **績效評估**：計算每期報酬並累積

### 回測設定

- **訓練起始**：1999/01
- **測試期間**：2013/11 ~ 2025/01（約 11 年）
- **預測頻率**：月度（每月重新訓練和預測）
- **驗證方式**：時間序列交叉驗證（滾動視窗）
- **投資組合規模**：13 種分組方式（1 支到 1051 支股票）

## 環境設置

### 系統需求

- Python 3.x
- 建議使用虛擬環境

### 安裝依賴套件

```bash
pip install pandas numpy openpyxl scikit-learn tensorflow xgboost
```

### 主要套件版本

- pandas 2.3.3
- numpy 2.3.5
- openpyxl 3.1.5
- tensorflow 2.20.0
- keras 3.12.0
- scikit-learn
- xgboost

## 使用方法

### 1. 建立真實 IC 基準

首先執行基準投資組合計算：

```bash
# 使用真實 IC 值構建多因子投資組合（主要程式）
python portfolio.py

# （可選）分析單一因子策略
python single.py
```

**功能說明**：
- `portfolio.py`：每期選擇真實 IC 絕對值最大的因子構建投資組合
- 輸出 `real.xlsx`，作為機器學習模型的對照基準
- `single.py`：固定使用單一因子（如 bm）分析其策略表現

確保以下資料檔案存在：
- bm.xlsx（帳面市值比因子及 IC 值）
- size.xlsx（公司規模因子及 IC 值）
- mom.xlsx（動量因子及 IC 值）

### 2. 模型訓練與預測

執行各模型的預測程式：

```bash
# 線性迴歸（注意：需手動修改程式碼中的參數分別預測 bm、size、mom）
python ols_predict.py

# 隨機森林（一次預測三個因子）
python rf_predict.py

# 神經網路（一次預測三個因子）
python nn_predict.py

# XGBoost（一次預測三個因子）
python xgboost_predict.py
```

**OLS 預測說明**：
- `ols_predict.py` 預設只預測 size 因子
- 需修改以下參數來預測不同因子：
  1. 檔案名稱（bm.xlsx / size.xlsx / mom.xlsx）
  2. 工作表名稱（bm補值、bmIC / size補值、sizeIC / mom補值、momIC）
  3. `n1, n2` 範圍（mom 因子需調整為 166, 307）
  4. `sheet.cell(row=3或4或5)` - 分別對應 bm、size、mom

### 3. 計算投資組合報酬

```bash
# 根據預測 IC 構建投資組合並計算報酬
python ols_return.py
python rf_return.py
python nn_return.py
python xgboost_return.py
```

**功能說明**：
- 讀取模型預測的 IC 值
- 每期選擇預測 IC 絕對值最大的因子
- 根據因子排名構建多空投資組合（13 種分組規模）
- 計算投資組合報酬並寫回 Excel 檔案

### 4. 績效分析與比較

```bash
# 批次處理所有模型的投資組合分析（包括 Real 基準）
python portfolio_analysis.py

# 整合所有模型結果到單一檔案
python integrate_excel.py

# 創建混淆矩陣評估預測準確性（比較預測 IC 與真實 IC）
python create_confusion_matrix.py
```

**分析說明**：
- `portfolio_analysis.py`：處理 Real.xlsx、OLS.xlsx、RF.xlsx、NN3.xlsx 等所有檔案
- `integrate_excel.py`：整合 6 個模型（OLS、RF、NN3、NN4、NN5、Real）的累積報酬到單一檔案
- `create_confusion_matrix.py`：評估預測 IC 的方向準確性（與真實 IC 比較）

## 評估指標

### 績效指標
- **累積報酬**：投資組合的累積收益
- **夏普比率**：風險調整後報酬
- **最大回撤**：最大虧損幅度

### 預測準確性指標
- **Accuracy**：整體預測準確率
- **Precision**：預測為正確的比例
- **Recall**：實際為正確的召回率
- **F1-score**：精確率和召回率的調和平均

## 專案特色

1. **真實 IC 基準對照**：提供真實 IC 構建的投資組合作為評估基準
2. **完整的研究流程**：從資料處理、模型訓練、預測到績效評估的端到端實現
3. **多模型比較**：比較傳統機器學習、深度學習與真實 IC 基準的績效
4. **動態因子選擇**：根據 IC 值（真實或預測）自動調整因子選擇
5. **穩健的回測**：使用時間序列交叉驗證避免前視偏誤
6. **自動化分析**：批次處理和結果整合工具

## 研究目的

- 建立真實 IC 投資組合作為績效基準
- 驗證機器學習模型預測 IC 的能力與價值
- 比較不同模型（OLS、RF、NN、XGBoost）的預測能力和投資績效
- 評估預測 IC 與真實 IC 的動態因子選擇策略差異
- 分析不同投資組合規模對績效的影響

## 參考文件

- [114智能交易授課大綱.pdf](114智能交易授課大綱.pdf)
- [智能交易_講義.pdf](智能交易_講義.pdf)
- [TEJPro及因子資料下載.pdf](TEJPro及因子資料下載.pdf)

## 注意事項

1. 本專案僅供學術研究和教學使用
2. 過去績效不代表未來表現
3. 實際投資需考慮交易成本、流動性等因素
4. 建議在虛擬環境中運行以避免套件衝突

## 授權聲明

本專案為學術研究用途，請勿用於商業目的。

## 聯絡資訊

如有任何問題或建議，歡迎聯繫專案維護者。
