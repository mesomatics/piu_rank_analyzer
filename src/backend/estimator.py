from .cols import *


class CountEstimator:
    """
    Rank to Count
    """
    def __call__(self, df):
        """
        Apply Linear Distribution.
        """
        df[COL_COUNT] = len(df) - df[COL_RANK].rank() + 1
        return df
