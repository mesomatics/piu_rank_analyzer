from scipy import stats
import numpy as np

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

class NormalEstimator(CountEstimator):
    """
    Rank to Count
    """
    def __init__(self, min_max_ratio=100.):
        self.min_max_ratio = min_max_ratio

    def __call__(self, df):
        """
        Apply Normal Distribution.
        """
        quantiles = np.linspace(0, 1, len(df) + 2)[1:-1]
        probs = stats.norm.ppf(quantiles)
        shift = (probs[-1] - self.min_max_ratio * probs[0]) / (self.min_max_ratio - 1)
        df[COL_COUNT] = np.flip(probs + shift)
        return df
