```bash
uv run pytest tests/test_futbolistas.py -q
..................                                                           [100%]
18 passed in 0.28s
```

```bash
pytest -q --cov=futbol --cov-report=term-missing --cov-fail-under=60 
................................                                                                         [100%]
================================================ tests coverage ================================================
_______________________________ coverage: platform darwin, python 3.14.7-final-0 _______________________________

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
futbol/__init__.py         0      0   100%
futbol/cli.py             38      1    97%   68
futbol/contracts.py       72      0   100%
futbol/preprocess.py       7      1    86%   6
----------------------------------------------------
TOTAL                    117      2    98%
Required test coverage of 60% reached. Total coverage: 98.29%
32 passed in 0.39s

```