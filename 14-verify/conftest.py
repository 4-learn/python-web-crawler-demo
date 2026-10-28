def pytest_addoption(parser):
    parser.addoption("--jsonl", action="store", default="output/N0060001.jsonl", help="要驗證的 JSONL 檔")
