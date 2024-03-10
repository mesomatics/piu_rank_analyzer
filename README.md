# PIU Stepchart Rank Analyzer

### Example

#### Import and initialize
```python
from src.backend.preprocessor import PiuRankPreprocessor
from src.backend.analyzer.single_month import SingleMonthAnalyzer

data = PiuRankPreprocessor().run()
sma = SingleMonthAnalyzer()
```

#### 레벨 선호도
```python
result = sma.level_preference(data[202403])
result.plot()
```
![download](https://github.com/mesomatics/piu_stepchart_rank_analyzer/assets/68718172/3fc90cba-1895-4577-9894-7dd8536e550d)

#### 노래 선호도
```python
song_pref, chart_pref = sma.song_preference(data[202403])
print(song_pref.head().to_markdown())
```
```
| title          |   Pref_Chart |
|:---------------|-------------:|
| 톰보이         |     0.983778 |
| 리틀 먼치킨    |     0.978036 |
| 플레이버 스텝! |     0.970018 |
| 시             |     0.968691 |
| 애프터 라이크  |     0.965806 |
```

#### 채보 선호도 (노래 선호도 adjusted)
```python
print(chart_pref.head().to_markdown()) ## 갓채보
```
```
|     | title                       |   level | mode   |
|----:|:----------------------------|--------:|:-------|
| 525 | 왓 해픈드                   |      20 | D      |
| 365 | 왓 해픈드                   |      23 | D      |
| 536 | 우츠시요 노 카제 feat. Kana |      20 | D      |
| 429 | 버터플라이                  |      17 | D      |
| 805 | 패러독스                    |      21 | S      |
```
```python
print(chart_pref.tail().to_markdown()) ## 똥채보
```
```
|      | title                     |   level | mode   |
|-----:|:--------------------------|--------:|:-------|
| 2173 | 다람쥐 헌 쳇바퀴에 타고파 |      24 | D      |
| 2810 | 우편마차                  |      22 | D      |
| 1616 | 웨딩 크래셔               |      21 | S      |
| 1525 | 유 앤 아이                |      24 | D      |
| 2273 | 모페모페                  |      25 | D      |
```
