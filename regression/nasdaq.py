import math

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates


def main():
    ixic = pd.read_csv("../data/IXIC.csv", usecols=['Date', 'Close'], parse_dates=['Date'])
    ixic.set_index('Date', inplace=True)
    ixic = ixic[ixic['Close'].notna()]

    gold = pd.read_csv("../data/WGC-GOLD_DAILY_USD.csv", parse_dates=['Date'])
    gold.set_index('Date', inplace=True)
    gold = gold[gold['Value'].notna()]

    d_index = pd.read_csv("../data/DX-Y.NYB.csv", usecols=['Date', 'Close'], parse_dates=['Date'])
    d_index.set_index('Date', inplace=True)
    d_index = d_index[d_index['Close'].notna()]

    # window_10 = 10
    # window_30 = 20
    # add_sma_col(ixic, "Close", window_10)
    # add_sma_col(ixic, "Close", window_30)
    # add_ema_col(ixic, "Close", window_30)

    # draw_two_graphs(d_index["Close"], "Dollar Index Close", ixic["Close"], "IXIC Close")
    # draw_two_graphs(gold["Value"], "Gold Price", ixic["Close"], "IXIC Close")
    draw_two_graphs(gold["Value"], "Gold Price", d_index["Close"], "Dollar Index Close")

    # ixic['Close'].plot()
    # ixic['Open'].plot(secondary_y=True, style='g')
    # plt.plot(ixic["Date"], ixic["Close"], label="IXIC")
    # plt.plot(ixic["Date"], ixic[create_sma_col_name("Close", window_30)], label="IXIC_SMA_%s" % window_30)
    # plt.plot(ixic["Date"], ixic[create_ema_col_name("Close", window_30)], label="IXIC_EMA_%s" % window_30)
    # plt.plot(gold["Date"], gold["Value"], label="GOLD")
    # draw_two_graphs("date", ixic["Date"], "nasdaq", ixic["Close"], d_index["Date"], "dollar index", d_index["Close"])
    # plt.legend()
    # plt.show()


def draw_two_graphs(lh_col, lh_label, rh_col, rh_label):
    fig, ax = plt.subplots()
    color = 'tab:red'
    lh_col.plot(color=color)
    ax.set_ylabel(lh_label, color=color)
    ax.tick_params(axis='y', labelcolor=color)

    color = 'tab:blue'
    rh_col.plot(secondary_y=True, color=color)
    ax.right_ax.set_ylabel(rh_label, color=color)
    ax.right_ax.tick_params(axis='y', labelcolor=color)

    locator = mdates.AutoDateLocator(minticks=3, maxticks=7)
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    fig.tight_layout()
    plt.show()


def add_sma_col(df, col_name, window):
    df[create_sma_col_name(col_name, window)] = df[col_name].rolling(window=window).mean()


def create_sma_col_name(col_name, window):
    return "sma_%s_%s" % (col_name, window)


def add_ema_col(df, col_name, window):
    df[create_ema_col_name(col_name, window)] = df[col_name].ewm(span=window, adjust=False).mean()


def create_ema_col_name(col_name, window):
    return "ema_%s_%s" % (col_name, window)


def extract_rows(start, end, df):
    return df.iloc[start:end], pd.concat([df.iloc[:start], df.iloc[end:]], ignore_index=True)


if __name__ == "__main__":
    main()
