# 智能交易系統 (Intelligent Trading System)

基於機器學習的台灣股票市場智能交易系統，使用多種 ML 模型預測股票因子的資訊係數（IC），並根據預測結果構建動態投資組合策略。

## 專案概述

本專案實現了完整的量化投資研究流程，從資料處理、模型訓練、預測到績效評估。核心策略是使用機器學習模型預測三個股票因子（帳面市值比、公司規模、動量）的未來資訊係數，並根據預測結果動態選擇最佳因子構建多空投資組合。

## 主要功能

- **多因子預測**：預測 bm（帳面市值比）、size（公司規模）、mom（動量）三個因子的 IC 值
- **動態因子選擇**：每期自動選擇預測 IC 絕對值最大的因子
- **投資組合構建**：基於因子排名建立多空投資組合（13種分組方式）
- **模型比較**：比較多種機器學習模型的預測能力
- **績效評估**：計算累積報酬並與大盤比較

## 專案結構

### 核心檔案

#### 投資組合計算
- **[portfolio.py](portfolio.py)**：多因子動態投資組合計算主程式
- **[single.py](single.py)**：單因子投資組合計算（用於單一因子策略測試）

#### 機器學習模型
- **[ols_predict.py](ols_predict.py)**：線性迴歸模型預測
- **[rf_predict.py](rf_predict.py)**：隨機森林模型預測
- **[nn_predict.py](nn_predict.py)**：深度神經網路模型預測
- **[xgboost_predict.py](xgboost_predict.py)**：XGBoost 梯度提升樹預測

#### 報酬計算
- **[ols_return.py](ols_return.py)**：計算 OLS 模型的投資組合報酬
- **[rf_return.py](rf_return.py)**：計算隨機森林模型的投資組合報酬
- **[nn_return.py](nn_return.py)**：計算神經網路模型的投資組合報酬
- **[xgboost_return.py](xgboost_return.py)**：計算 XGBoost 模型的投資組合報酬

#### 分析工具
- **[portfolio_analysis.py](portfolio_analysis.py)**：批次處理投資組合分析系統
- **[integrate_excel.py](integrate_excel.py)**：整合多個模型結果到單一 Excel 檔案
- **[create_confusion_matrix.py](create_confusion_matrix.py)**：創建混淆矩陣工作表，評估預測準確性

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
   - 基準模型，提供線性預測能力

2. **隨機森林 (Random Forest)**
   - 使用 `sklearn.ensemble.RandomForestRegressor`
   - 參數：`max_depth=3, n_estimators=100`
   - 捕捉非線性關係

3. **深度神經網路 (Neural Network)**
   - 使用 TensorFlow/Keras
   - 架構：5 層全連接網路 (32→16→8→1)
   - L1 正則化防止過擬合
   - 早停機制優化訓練

4. **XGBoost**
   - 使用 `xgboost.XGBRegressor`
   - 參數：`n_estimators=100, max_depth=3, learning_rate=0.05`
   - 梯度提升樹模型

### 投資策略

1. **訓練階段**：使用歷史資料（1999/01 起）訓練模型
2. **預測階段**：預測下期三個因子的 IC 值
3. **因子選擇**：選擇預測 IC 絕對值最大的因子
4. **股票排名**：根據選定因子對股票進行排名
5. **組合構建**：建立多空投資組合（做多高排名，做空低排名）
6. **績效評估**：計算報酬並累積

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

### 1. 資料準備

確保以下資料檔案存在：
- bm.xlsx（帳面市值比因子）
- size.xlsx（公司規模因子）
- mom.xlsx（動量因子）

### 2. 模型訓練與預測

執行各模型的預測程式：

```bash
# 線性迴歸
python ols_predict.py

# 隨機森林
python rf_predict.py

# 神經網路
python nn_predict.py

# XGBoost
python xgboost_predict.py
```

### 3. 計算投資組合報酬

```bash
# 計算各模型的報酬
python ols_return.py
python rf_return.py
python nn_return.py
python xgboost_return.py
```

### 4. 分析結果

```bash
# 批次分析投資組合
python portfolio_analysis.py

# 整合所有模型結果
python integrate_excel.py

# 創建混淆矩陣評估預測準確性
python create_confusion_matrix.py
```

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

1. **完整的研究流程**：從資料處理到績效評估的端到端實現
2. **多模型比較**：比較傳統機器學習與深度學習模型
3. **動態策略**：根據預測自動調整因子選擇
4. **穩健的回測**：使用時間序列交叉驗證避免前視偏誤
5. **自動化分析**：批次處理和結果整合工具

## 研究目的

- 驗證機器學習模型在因子投資中的應用價值
- 比較不同模型的預測能力和投資績效
- 評估動態因子選擇策略的有效性
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
