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
#### Level Preference
```python
result = sma.level_preference(data[202403])
result.plot()
```
![download](https://github.com/mesomatics/piu_stepchart_rank_analyzer/assets/68718172/3fc90cba-1895-4577-9894-7dd8536e550d)
---
#### Song Preference
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
```python
## 더블 18렙 이상만 분석
song_pref, _ = sma.song_preference(data[202403], query="mode == 'D' and level >= 18")
print(song_pref.head().to_markdown())
```
```python
| title                                    |   Pref_Chart |
|:-----------------------------------------|-------------:|
| 스테이저                                 |     0.993243 |
| 사이먼 세이즈, 유로댄스!! (feat. Sara☆M) |     0.990564 |
| 리틀 먼치킨                              |     0.989702 |
| 서든 어페어런스 이미지                   |     0.983097 |
| 톰보이                                   |     0.980214 |
```
---
#### Chart Preference (Song preference adjusted)
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
