import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Displayer:

    # rate = {0, 1}, data = list
    @staticmethod
    def lowPassFilter(data, rate):
        tmp_data = data[0]
        filter_data = []
        filter_data.append(tmp_data)
        for i in range(1, len(data)):
            tmp_data = tmp_data * rate + data[i] * (1.0 - rate)
            filter_data.append(tmp_data)
        return filter_data

    @staticmethod
    def smoothDF(df):
        # nans = np.where(np.empty_like(df.values), np.nan, np.nan)
        # data = np.hstack([nans, df.values]).reshape(-1, df.shape[1])
        # df = pd.DataFrame(data, columns=df.columns)
        # df = df.interpolate(method='spline', order=1)
        for col in df:
            li = df[col].to_list()
            li = Displayer.lowPassFilter(li, 0.8)
            df[col] = li
        return df

    @staticmethod
    def displayData(df):
        df = Displayer.smoothDF(df)
        ax = df.plot.line()
        ax.set_title("Word trend by day")
        ax.set_ylabel("occurence")
        plt.show()