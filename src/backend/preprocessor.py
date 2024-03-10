from .cols import *

class PiuRankPreprocessor:
    def _preprocess(self, df):
        df.query("pattern != 'C'", inplace=True)
        df[COL_MODE] = df["pattern"].str[:1]
        df[COL_LEVEL] = df["pattern"].str[1:].astype(int)
        df.rename(columns={"song": COL_TITLE}, inplace=True)
        return df
    
    def run(self):
        pass
