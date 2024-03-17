import pandas as pd

from ..cols import *
from .preference import PreferenceModel


class SingleMonthAnalyzer:
    def __init__(self):
        self._mode_preference = None
        self._level_preference = None
        self._song_preference = None

    def set_df(self, df):
        self.__init__()
        self.df = df.copy()

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
            if getattr(self, f"_{func.__name__}") is None:
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

    def decompose(self):
        result = self.df.merge(self.mode_preference)  \
                        .merge(self.level_preference) \
                        .merge(self.song_preference)

        result["Pick_Ratio"] = result["count"] / result["count"].sum()

        level_total_pref = result.groupby("pattern")["Song_Preference"].sum()
        level_total_pref.name = "Level_total_pref"
        level_total_pref = level_total_pref.reset_index()
        result = result.merge(level_total_pref)
        result["Song_Preference_in_Level"] = result["Song_Preference"] / result["Level_total_pref"]
        result["Chart_Preference"] = result.eval(
            "Pick_Ratio / (Mode_Preference * Level_Preference * Song_Preference_in_Level)"
        )
        result.drop(columns="Level_total_pref", inplace=True)
        return result
