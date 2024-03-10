import pandas as pd

from ..cols import *


class SingleMonthAnalyzer:
    def level_preference(self, df, query=None):
        """
        Parameters
        ----------
        df: DataFrame
        
        query: str, optional
        """
        if query is not None:
            df = df.query(query)
        def count_(mode):
            df_sub = df.query(f"`{COL_MODE}` == @mode")
            count = df_sub.groupby(COL_LEVEL)[COL_COUNT].sum()
            count.name = mode
            return count
        count_s = count_("S")
        count_d = count_("D")
        count_all = pd.concat([count_s, count_d], axis=1)
        count_all = count_all.fillna(0).astype(int)
        count_all["ALL"] = count_all.sum(axis=1)
        return count_all

    def song_preference(self, df, query=None):
        df = df.copy()
        if query is not None:
            df = df.query(query)
        df["Pref_Chart"] = 1 - df.groupby([COL_LEVEL, COL_MODE])[COL_COUNT].rank(ascending=False, pct=True)
        df["Pref_Song"] = df.groupby(COL_TITLE)["Pref_Chart"].transform("mean")
        pref_song = df.groupby(COL_TITLE)["Pref_Chart"].mean().sort_values(ascending=False)
        df["Pref_Diff"] = df["Pref_Chart"] - df["Pref_Song"]
        df.sort_values("Pref_Diff", inplace=True)
        return pref_song, df
