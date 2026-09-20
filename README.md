docker compose up --build

对外入口是 /health 和 /query ，不要换。
核对用 python check.py 。

ledger/books.json 是最终对外账本，只放真账并带 version；
样例账独立放 samples/books.json ，不进最终层。
启动时用 LEDGER_VERSION 与账本 version 核对，缺失或对不上即非零退出。
