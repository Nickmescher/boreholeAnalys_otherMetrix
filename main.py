import pandas as pd
import algorythm as alg
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.express as px
import os
import numpy as np
from scipy.signal import find_peaks

# df.drop(df.index[1:50], inplace=True) на случай если нужно будет удалить
# df.reset_index(inplace=True)

fig = go.Figure()
fig = make_subplots(rows=3, cols=1)
fig2 = go.Figure()
fig2 = make_subplots(rows=1, cols=1)
fig4 = go.Figure()
fig4 = make_subplots(rows=3, cols=1, subplot_titles=("Изначальные данные в периоде максимального процента отдачи", "Общий график", "Соотношение дифференциалов процента открытия клапана и расхода газа"))
fig5 = go.Figure()
fig5 = make_subplots(rows=3, cols=1)
fig3 = go.Figure()
fig3 = make_subplots(rows=2, cols=1)  # создание графиков

percentagedf = "Процент открытия"
time = "time"
chargedf = "Расход газа"

p = pd.read_csv(r"E:\nickmescher\analys data\cache1\cache\501 (2021-09-13 00_00_00).csv",
                encoding='utf8', sep=';',
                decimal=',', parse_dates=[time],
                usecols=[time, percentagedf, chargedf])

p[[percentagedf, chargedf]] = p[[percentagedf, chargedf]].astype(float)

p = p.loc[p[percentagedf] > 0]
p = p.loc[p[percentagedf] < 100]
p = p.loc[p[chargedf] > 0]
p = p.loc[p[chargedf] < 100]

p.reset_index(drop=True, inplace=True)

fig2 = px.scatter(x=p[time],
                  y=p[chargedf],
                  trendline="rolling", trendline_options=dict(function="median", window=100),
                  trendline_color_override="red")

p['Q_diff'] = p[chargedf].diff()
p['Q_approx'] = pd.Series(fig2.data[1].y)
p['Q_DiffApproxed'] = p['Q_approx'].diff()
p['Perc_Diff'] = p[percentagedf].diff()

normalized_df = pd.DataFrame({'Q_approx': p['Q_approx'],
                              'Perc': p[percentagedf],
                              'Q_DiffApproxed': p['Q_DiffApproxed'],
                              'Perc_Diff': p['Perc_Diff'],
                              "Q_OrigDiff": p['Q_diff'],
                              'Q_Orig': p[chargedf]})

normalized_df = (normalized_df - normalized_df.mean()) / normalized_df.std()

normalized_df["percForPeaks"] = 0

for n in enumerate(normalized_df["Perc_Diff"]):
    if n[1] < 0:
        normalized_df["percForPeaks"][n[0]] = normalized_df["Perc_Diff"][n[0]] * -1
    else:
        normalized_df["percForPeaks"][n[0]] = normalized_df["Perc_Diff"][n[0]]

fig.append_trace(go.Scatter(
    x=p[time],
    y=p[percentagedf],
    name="Процент открытия",
), row=1, col=1)

fig.append_trace(go.Scatter(
    x=p[time],
    y=p[chargedf],
    name="Расход газа",
), row=2, col=1)

fig.append_trace(go.Scatter(
    x=fig2.data[1].x,
    y=fig2.data[1].y,
    name="approximated",
), row=3, col=1)  # fig

fig3.append_trace(go.Scatter(
    x=p[time],
    y=normalized_df['Perc'],
    name='Percentage'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p[time],
    y=normalized_df['Q_approx'],
    name='Q'
), row=1, col=1)

fig3.append_trace(go.Scatter(
    x=p[time],
    y=normalized_df['percForPeaks'],
    name='percForPeaks'
), row=2, col=1)

fig3.append_trace(go.Scatter(
    x=p[time],
    y=normalized_df['Perc_Diff'],
    name='Perc_Diff'
), row=2, col=1)

fig3.append_trace(go.Scatter(
    x=p[time],
    y=normalized_df['Q_OrigDiff'],
    name='Q_Diff'
), row=2, col=1)

# fig3

indices = find_peaks(normalized_df["percForPeaks"], threshold=1.15)[0]

fig3.append_trace(go.Scatter(
    x=p[time][indices],
    y=[normalized_df["percForPeaks"][j] for j in indices],
    mode='markers',
    marker=dict(
        size=8,
        color='red',
        symbol='cross'
    ),
    name='Detected Peaks'
), row=2, col=1)  # fig3 + peaks

fig.update_layout(title_text="Скважина 501")
fig2.update_layout(title_text="Скважина 501")
fig3.update_layout(title_text="Скважина 501")

fig.show()
fig3.show()

normalized_df["Time"] = p[time]

quan = len(normalized_df["Perc_Diff"]) - 1

percs = []

for n in enumerate(indices[::-1]):
    percs.append(p[percentagedf][n[1]])
    print(percs)

answers = alg.algorythm(normalized_df, indices)
print(answers)

for n in enumerate(answers):
    print(p[percentagedf][n[1]])

if len(answers) > 0:
    endanswer = alg.comparing(p, answers)

    fig4.append_trace(go.Scatter(
        x=p[time][endanswer - 50:endanswer + 50],
        y=p[percentagedf][endanswer - 50:endanswer + 50],
        name='Percentage'
    ), row=1, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time][endanswer - 50:endanswer + 50],
        y=p[chargedf][endanswer - 50:endanswer + 50],
        name='Q'
    ), row=1, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time],
        y=p[percentagedf],
        name="Процент открытия",
    ), row=2, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time],
        y=p[chargedf],
        name="Расход газа",
    ), row=2, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time][endanswer - 50:endanswer + 50],
        y=normalized_df['percForPeaks'][endanswer - 50:endanswer + 50],
        name='percForPeaks'
    ), row=3, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time][endanswer - 50:endanswer + 50],
        y=normalized_df['Perc_Diff'][endanswer - 50:endanswer + 50],
        name='Perc_Diff'
    ), row=3, col=1)

    fig4.append_trace(go.Scatter(
        x=p[time][endanswer - 50:endanswer + 50],
        y=normalized_df['Q_OrigDiff'][endanswer - 50:endanswer + 50],
        name='Q_Diff'
    ), row=3, col=1)

    # fig4

    if not os.path.exists("images"):
        os.mkdir("images")
    titleans = "Процен отдачи скв 4004 "
    dateans = p[time][endanswer]
    percans = p[percentagedf][endanswer]
    titleans += str(dateans)
    titleans += " "
    titleans += str(percans)
    print(titleans)

    fig4.update_layout(title_text=titleans)
    fig4.show()
    fig4.write_image("images/report_4004.pdf")
else:
    if not os.path.exists("images"):
        os.mkdir("images")
    maxperc = max(p["Процент открытия"], default="100")
    titleans = "Максимальный обнаруженный процент" + str(maxperc)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=p[percentagedf],
        name="Процент открытия",
    ), row=1, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=p[chargedf],
        name="Расход газа",
    ), row=1, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=normalized_df['Perc'],
        name='Percentage'
    ), row=2, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=normalized_df['Q_approx'],
        name='Q'
    ), row=2, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=normalized_df['percForPeaks'],
        name='percForPeaks'
    ), row=3, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=normalized_df['Perc_Diff'],
        name='Perc_Diff'
    ), row=3, col=1)

    fig5.append_trace(go.Scatter(
        x=p[time],
        y=normalized_df['Q_OrigDiff'],
        name='Q_Diff'
    ), row=3, col=1)

    fig5.update_layout(title_text=titleans)
    fig5.write_image("images/report_4004.pdf")
    print(titleans)

print()
