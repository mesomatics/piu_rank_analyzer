import os

import pandas as pd

from .cols import *
from .estimator import LinearEstimator, NormalEstimator


class PiuRankPreprocessor:
    def __init__(self, estimator=NormalEstimator):
        self.count_estimator = estimator()

    def _read_files(self, path):
        files = sorted(os.listdir(path))
        data = {}
        for file in files:
            df = pd.read_csv(os.path.join(path, file))
            month = int(file[:6])
            data[month] = df
        return data

    def _preprocess(self, df):
        df.query("pattern.str[0] in ['S', 'D']", inplace=True)
        df[COL_MODE] = df["pattern"].str[:1]
        df[COL_LEVEL] = df["pattern"].str[1:].astype(int)
        df.rename(columns={"song": COL_TITLE}, inplace=True)
        return df
    
    def run(self, path="data"):
        """
        Returns
        -------
        data: dict
            key: yearmonth(int), value: DataFrame
        """
        data = self._read_files(path)
        for month, df in data.items():
            df = self._preprocess(df)
            data[month] = self.count_estimator(df)
        return data
