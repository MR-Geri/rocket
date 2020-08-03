import plotly.graph_objs as go
import plotly
from plotly.subplots import make_subplots

import numpy as np
import pandas as pd


accuracy = 0.01


def main():
    fig = go.Figure()
    fig.update_yaxes(range=[0, 708000], zeroline=True, zerolinewidth=2, zerolinecolor='LightPink')
    fig.update_xaxes(range=[10, 125.15 + 50], zeroline=True, zerolinewidth=2, zerolinecolor='#008000')
    fig.update_layout(legend_orientation="h",
                      legend=dict(x=.5, xanchor="center"),
                      title="График",
                      xaxis_title="x",
                      yaxis_title="y",
                      margin=dict(l=0, r=0, t=30, b=0))
    m0 = 50000  # кг
    P = 700000  # KH
    i = 2700  # м/c
    m_t0 = 40000
    P_ypr = 5  # H
    le = 15  # м
    d = 1  # м
    R_x = 100  # H
    R_y = 0
    x = 0
    y = 0
    omega = 0
    fit = 0
    V_x = 0
    V_y = 0
    g = 9.81
    x_m = []
    y_m = []
    time = [int(i) for i in range(601)]
    v_main_x = []
    v_main_y = []
    v = []
    # p_ypr and p со старта и до конца топлива
    # if p_ypr = 0: omega = 0
    # t(0...600)c
    for t in time:
        m_Tt = m_t0 - (P + P_ypr) / i * t
        m_PH = m0 - m_t0 + m_Tt if m_Tt > 0 else m0 - m_t0
        P_t = P if m_Tt > 0 else 0
        P_ypr = P_ypr if m_Tt > 0 else 0
        M_ypr = P_ypr * le / 2
        # I_i = 0.25 * m_PH * ((d / 2) ** 2) + (1 / 12) * m_PH * (le ** 2)
        I_i = (1 / 16) * m_Tt * (d ** 2) + (1 / 12) * m_Tt * (le ** 2)
        d_omega = M_ypr / I_i
        omega = omega + d_omega if m_Tt > 0 else 0
        omega = 0 if P_ypr <= 0 else omega
        fit += omega
        V_x += ((P_t - R_x) * np.cos(np.pi / 2 - fit) - P_ypr * np.sin(np.pi / 2 - fit)) / m_PH
        V_y += ((P_t - R_y) * np.sin(np.pi / 2 - fit) + P_ypr * np.cos(np.pi / 2 - fit) - m_PH * g) / m_PH
        x += V_x
        y += V_y
        x_m.append(x)
        y_m.append(y)
        v_main_x.append(V_x)
        v_main_y.append(V_y)
        v.append(np.sqrt(V_x ** 2 + V_y ** 2))

    fig.add_trace(go.Scatter(x=x_m, y=y_m, name='y=f(x)'))
    fig.add_trace(go.Scatter(x=time, y=x_m, name='x(t)'))
    fig.add_trace(go.Scatter(x=time, y=y_m, name='y(t)'))
    fig.add_trace(go.Scatter(x=time, y=v_main_x, name='V_y(t)'))
    fig.add_trace(go.Scatter(x=time, y=v_main_y, name='V_x(t)'))
    fig.add_trace(go.Scatter(x=time, y=v, name='V(t)'))
    plotly.offline.plot(fig, filename='file.html')
    fig.show()


main()
