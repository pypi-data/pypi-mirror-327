# parquet_to_excel
A tool to convert parquet file to excel file in rust with constant memory, both a single parquet file and a folder of parquet files are supported.
You can also use python or rust to call it. The python package name is parquet_to_excel too. you can install it by `pip install parquet_to_excel`. If you could not install this package correctly, you can try to install rust and maturin (`pip install maturin`) first. Then you can try again.

# Functions
1. parquet_file_to_xlsx: convert a single parquet file to an excel file
2. parquet_files_to_xlsx: convert a folder of parquet files to an excel file

# A Python Example
```python
from parquet_to_excel import parquet_file_to_xlsx, parquet_files_to_xlsx

# the last three arguments are optional
parquet_file_to_xlsx(r"data\result\qid=160\a.parquet", r"out1.xlsx", "data", "", {"ddbm": "地点编码"})
parquet_files_to_xlsx(r"data\result\qid=160", r"out2.xlsx", "", "scfs", {"ddbm": "地点编码"})
```
