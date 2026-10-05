def pytest_addoption(parser):
    parser.addoption("--jsonl", action="store", default="output.jsonl", help="要驗證的 JSONL 檔")
