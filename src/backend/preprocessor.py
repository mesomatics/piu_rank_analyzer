import os

import pandas as pd

from .cols import *
from .estimator import CountEstimator


class PiuRankPreprocessor:
    def _read_files(self, path):
        files = sorted(os.listdir(path))
        data = {}
        for file in files:
            df = pd.read_csv(os.path.join(path, file))
            month = int(file[:6])
            data[month] = df
        return data

    def _preprocess(self, df):
        df.query("pattern != 'C'", inplace=True)
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
        ce = CountEstimator()
        for month, df in data.items():
            df = self._preprocess(df)
            data[month] = ce(df)
        return data
