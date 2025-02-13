from parquet_to_excel import parquet_file_to_xlsx, parquet_files_to_xlsx

# parquet_file_to_xlsx(r"D:\Projects\RustTool\data\.duck\qy_tempdata\qid=142\part0.parquet", r"D:\Felix\Desktop\out1.xlsx", "data", "")
# parquet_file_to_xlsx(r"D:\Projects\RustTool\data\.duck\qy_tempdata\qid=142\part0.parquet", r"D:\Felix\Desktop\out2.xlsx", "", "scfs")
parquet_files_to_xlsx(r"D:\Projects\TornadoSrv\data\result\qid=160", r"D:\Felix\Desktop\out1.xlsx", "data", "", {"ddbm": "地点编码"})
parquet_files_to_xlsx(r"D:\Projects\TornadoSrv\data\result\qid=160", r"D:\Felix\Desktop\out2.xlsx", "", "scfs", {"ddbm": "地点编码"})