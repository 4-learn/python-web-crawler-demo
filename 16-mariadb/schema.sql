-- 16｜法規條文資料表
-- 一條條文一列；(pcode, slug) 是唯一鍵，重複執行 upsert 不會產生重複資料。
CREATE TABLE IF NOT EXISTS law_articles (
  id           INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  pcode        VARCHAR(16)  NOT NULL,
  law_name     VARCHAR(100) NOT NULL,
  slug         VARCHAR(16)  NOT NULL,
  article_no   VARCHAR(32)  NOT NULL,
  chapter      VARCHAR(200) NOT NULL DEFAULT '',
  content      TEXT         NOT NULL,
  source_url   VARCHAR(500) NOT NULL,
  content_hash CHAR(64)     NOT NULL,
  fetched_at   DATETIME     NOT NULL,
  updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_article (pcode, slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
