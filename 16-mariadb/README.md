# 16｜寫入 MariaDB

沿用 MariaDB 課的環境。先建立資料庫與帳號（老師或有權限者執行一次）：

```sql
CREATE DATABASE IF NOT EXISTS crawler_course CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'crawler'@'localhost' IDENTIFIED BY '請自訂密碼';
GRANT SELECT, INSERT, UPDATE, CREATE ON crawler_course.* TO 'crawler'@'localhost';
```

安裝 Connector：

```bash
sudo apt install -y libmariadb-dev
pip install mariadb==1.1.14
```

執行：

```bash
export DB_USER=crawler DB_PASS='你的密碼' DB_NAME=crawler_course
python load_jsonl.py ../05-pagination/N0060001.jsonl   # 第一次：新增 61
python load_jsonl.py ../05-pagination/N0060001.jsonl   # 第二次：未變 61
```
