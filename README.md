# PIU Stepchart Rank Analyzer

### Example

#### Import and initialize
```python
from src.backend.preprocessor import PiuRankPreprocessor
from src.backend.analyzer.single_month import SingleMonthAnalyzer

data = PiuRankPreprocessor().run()
sma = SingleMonthAnalyzer()
```
---
#### Example
```python
df = data[202402]
sma.set_df(df)
result = sma.decompose()
```

#### Level Preference
```python
for _, df_sub in sma.level_preference.groupby("mode"):
    df_sub.set_index("level")["Level_Preference"].plot()
```
![level](https://github.com/mesomatics/piu_stepchart_rank_analyzer/assets/68718172/4bcbd8d8-e9e1-4a84-b984-6848ada48034)

#### Song Preference
```python
print(sma.song_preference.head(10).to_markdown())
```
```
|    | title                        |   Song_Preference |
|---:|:-----------------------------|------------------:|
|  0 | 애프터 라이크                |           1.87534 |
|  1 | 유포리아닉                   |           1.78086 |
|  2 | 요! 세이!! 페어리!!!         |           1.73395 |
|  3 | 일레븐                       |           1.73201 |
|  4 | 테디베어                     |           1.71719 |
|  5 | 누드                         |           1.68599 |
|  6 | 얼론                         |           1.62461 |
|  7 | 진폐증 ft. Kagamine Len/GUMI |           1.59484 |
|  8 | 비행기                       |           1.57226 |
|  9 | 파이렛                       |           1.54802 |
```

