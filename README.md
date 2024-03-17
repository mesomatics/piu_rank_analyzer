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
