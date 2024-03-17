import pandas as pd

from ..cols import *
from .preference import PreferenceModel


class SingleMonthAnalyzer:
    def __init__(self):
        self.full = ["S", "D"]
        self.basic = ["E", "N", "H", "V"]

    def set_df(self, df):
        self.df = df.query("mode in @self.full").copy()

    def _calc_mode_preference(self):
        count = self.df.groupby(COL_MODE)[COL_COUNT].sum()
        count = count / count.sum()
        count.name = "Mode_Preference"
        self._mode_preference = count.reset_index()

    def _calc_level_preference(self):
        count = self.df.groupby([COL_MODE, COL_LEVEL])[COL_COUNT].sum() / \
                self.df.groupby(COL_MODE)[COL_COUNT].sum()
        count.name = "Level_Preference"
        self._level_preference = count.reset_index()

    def _calc_song_preference(self):
        model = PreferenceModel(self.df)
        result = model.run()
        result = result.reset_index()
        self._song_preference = result

    def preference_getter(func):
        func_name = func.__name__
        @property
        def getter(self):
            if not hasattr(self, f"_{func.__name__}"):
                getattr(self, f"_calc_{func.__name__}")()
            return getattr(self, f"_{func.__name__}")
        return getter

    @preference_getter
    def mode_preference(self):
        pass

    @preference_getter
    def level_preference(self):
        pass

    @preference_getter
    def song_preference(self):
        pass
