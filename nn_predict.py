import os
import openpyxl
import pandas as pd
import numpy as np
from openpyxl import load_workbook
from keras.layers import Dense
from keras.models import Sequential
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import EarlyStopping

""" Step1 引入需要的套件(已完成) """

""" Step2 定義路徑 """
os.chdir(r'C:\Users\raymo\Desktop\SCU work\智能交易')

""" Step3 關閉 GPU 運行(改用 CPU) """
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

""" Step3 建立 隨機種子 模型 """
seed = 999
os.environ['PYTHONHASHSEED'] = str(seed)
import random
random.seed(seed)
np.random.seed(seed)
tf.random.set_seed(seed)

""" 建立 NN 模型 """
def create_model(input_dim):
    M = Sequential([
        Dense(32, activation='relu', input_shape=(input_dim,), 
              kernel_regularizer=regularizers.l1(1e-4)),
        Dense(16, activation='relu'),
        Dense(8, activation='relu'),
        #Dense(4, activation='relu'),
        #Dense(2, activation='relu'),
        Dense(1)
    ])
    return M

""" Step4 預測IC值 """
# 讀取 Excel 檔案
workbook = openpyxl.load_workbook("NN3.xlsx")
sheet = workbook["預測IC"]

n0 = 48  # 驗證集固定4年

""" 預測 bm 的IC """
df_x = pd.read_excel('bm.xlsx', sheet_name="bm補值")
df_y = pd.read_excel('bm.xlsx', sheet_name="bmIC")
df_x = df_x.T
df_y = df_y.T
df_x = df_x.iloc[2:,:]
df_y = df_y.iloc[2:,:]
n1, n2 = 178, 319

for n in range(n1, n2):
    X = df_x.iloc[0:n,:].values
    Y = df_y.iloc[1:n+1,:].values.ravel()
    test_X = df_x.iloc[n:n+1,:].values
    
    # M.fit不支援 ndarray,故須轉成 float64
    X = X.astype('float64')
    Y = Y.astype('float64')
    test_X = test_X.astype('float64')
    
    # 訓練集
    X_train = X[0:n-n0,:]
    Y_train = Y[0:n-n0]
    # 驗證集固定4年 n0=4*12=48
    X_val = X[n-n0:n,:]
    Y_val = Y[n-n0:n]
    
    # 建立新模型
    M = create_model(X.shape[1])
    # ⭐ 每次都創建新的 optimizer!
    adam = Adam(learning_rate=0.01)
    M.compile(optimizer=adam, loss='mean_squared_error')
    
    # ⭐ 每次都創建新的 early_stopping!
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        mode='min',
        restore_best_weights=True
    )
    
    M.fit(X_train, Y_train,
          validation_data=(X_val, Y_val),
          epochs=100,
          batch_size=32,
          callbacks=[early_stopping],
          verbose=0)
    
    predIC = M.predict(test_X, verbose=0)
    sheet.cell(row=3, column=n-n1+3, value=float(predIC[0,0]))
    print(n)

""" 預測 size 的IC """
df_x = pd.read_excel('size.xlsx', sheet_name="size補值")
df_y = pd.read_excel('size.xlsx', sheet_name="sizeIC")
df_x = df_x.T
df_y = df_y.T
df_x = df_x.iloc[2:,:]
df_y = df_y.iloc[2:,:]
n1, n2 = 178, 319

for n in range(n1, n2):
    X = df_x.iloc[0:n,:].values
    Y = df_y.iloc[1:n+1,:].values.ravel()
    test_X = df_x.iloc[n:n+1,:].values
    
    X = X.astype('float64')
    Y = Y.astype('float64')
    test_X = test_X.astype('float64')
    
    X_train = X[0:n-n0,:]
    Y_train = Y[0:n-n0]
    X_val = X[n-n0:n,:]
    Y_val = Y[n-n0:n]
    
    M = create_model(X.shape[1])
    adam = Adam(learning_rate=0.01)
    M.compile(optimizer=adam, loss='mean_squared_error')
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        mode='min',
        restore_best_weights=True
    )
    
    M.fit(X_train, Y_train,
          validation_data=(X_val, Y_val),
          epochs=100,
          batch_size=32,
          callbacks=[early_stopping],
          verbose=0)
    
    predIC = M.predict(test_X, verbose=0)
    sheet.cell(row=4, column=n-n1+3, value=float(predIC[0,0]))
    print(n)

""" 預測 mom 的IC """
df_x = pd.read_excel('mom.xlsx', sheet_name="mom補值")
df_y = pd.read_excel('mom.xlsx', sheet_name="momIC")
df_x = df_x.T
df_y = df_y.T
df_x = df_x.iloc[2:,:]
df_y = df_y.iloc[2:,:]
n1, n2 = 166, 307

for n in range(n1, n2):
    X = df_x.iloc[0:n,:].values
    Y = df_y.iloc[1:n+1,:].values.ravel()
    test_X = df_x.iloc[n:n+1,:].values
    
    X = X.astype('float64')
    Y = Y.astype('float64')
    test_X = test_X.astype('float64')
    
    X_train = X[0:n-n0,:]
    Y_train = Y[0:n-n0]
    X_val = X[n-n0:n,:]
    Y_val = Y[n-n0:n]
    
    M = create_model(X.shape[1])
    adam = Adam(learning_rate=0.01)
    M.compile(optimizer=adam, loss='mean_squared_error')
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=5,
        mode='min',
        restore_best_weights=True
    )
    
    M.fit(X_train, Y_train,
          validation_data=(X_val, Y_val),
          epochs=100,
          batch_size=32,
          callbacks=[early_stopping],
          verbose=0)
    
    predIC = M.predict(test_X, verbose=0)
    sheet.cell(row=5, column=n-n1+3, value=float(predIC[0,0]))
    print(n)

""" 存檔 """
workbook.save("NN3.xlsx")