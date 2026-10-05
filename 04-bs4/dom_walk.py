"""04｜HTML 是一棵樹：parent、children、next_sibling。

執行：python dom_walk.py
"""
from bs4 import BeautifulSoup

html = """
<section class="articles">
  <article class="article" data-slug="1">
    <h3 class="article-no"><a href="articles/1.html">第 1 條</a></h3>
    <p class="chapter">第一章 總則</p>
    <div class="article-content"><p>第一段</p><p>第二段</p></div>
  </article>
</section>
"""
soup = BeautifulSoup(html, "html.parser")
a = soup.select_one("h3.article-no a")
print("文字：", a.get_text())
print("屬性 href：", a["href"])
print("父節點：", a.parent.name, a.parent["class"])
article = a.find_parent("article")
print("往上找 article：", article["data-slug"])
print("h3 的下一個兄弟元素：", article.h3.find_next_sibling().get_text())
paragraphs = [p.get_text() for p in article.select(".article-content p")]
print("多段內容用換行接起來：", "\n".join(paragraphs))
