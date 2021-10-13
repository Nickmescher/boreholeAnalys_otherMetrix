import pandas as pd
import numpy as np





def algorythm(df, indices):
    answers = []
    for n in enumerate(indices[::-1]):
        if df["Perc_Diff"][n[1]] > 0:
            if df["Q_OrigDiff"][n[1]] > df["Q_OrigDiff"][n[1] + 1] and df["Q_OrigDiff"][n[1]] > df["Q_OrigDiff"][n[1] - 1]  or (df["Q_OrigDiff"][n[1] + 1] > 0 and df["Q_OrigDiff"][n[1] + 1] >
                              df["Q_OrigDiff"][n[1]]):
                print("найден пик на")
                print(df["Time"][n[1]])
                answers.append(n[1])
        else:
            if df["Q_OrigDiff"][n[1]] < df["Q_OrigDiff"][n[1] + 1] and df["Q_OrigDiff"][n[1]] < df["Q_OrigDiff"][n[1] - 1] or (df["Q_OrigDiff"][n[1] + 1] < 0 and df["Q_OrigDiff"][n[1] + 1] <
                             df["Q_OrigDiff"][n[1]]):
                print("найден пик на")
                print(df["Time"][n[1]])
                answers.append(n[1])
    return answers

def comparing(df, rightInd):
    a = df["Процент открытия"][rightInd[0]]
    b = 0
    for n in enumerate(rightInd):
        if df["Процент открытия"][n[1]] > a:
            a = df["Процент открытия"][n[1]]
            b = n[1]
    return b