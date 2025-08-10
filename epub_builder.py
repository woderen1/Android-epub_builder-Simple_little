# -*- coding: utf-8 -*-
import os
import re
import glob
from ebooklib import epub

# ===== 用户配置区 =====
BOOK_TITLE = "我的电子书"      # 书名
AUTHOR = "佚名"               # 作者
COVER_SEARCH_DIR = "/storage/emulated/0/Download/eebook/covers"  # 封面搜索目录
CHAPTERS_DIR = "/storage/emulated/0/Download/eebook/chapters"    # 章节文本目录
# =====================

def find_cover_image():
    """自动搜索封面图片（优先选择cover.jpg/png）"""
    for ext in ['jpg', 'jpeg', 'png']:
        cover_path = os.path.join(COVER_SEARCH_DIR, f'cover.{ext}')
        if os.path.exists(cover_path):
            return cover_path
    return None  # 无封面时返回None

def load_chapters():
    """批量加载章节文本（按文件名排序）"""
    chapters = []
    txt_files = sorted(glob.glob(os.path.join(CHAPTERS_DIR, "*.txt")))
    for idx, file_path in enumerate(txt_files):
        chapter_title = os.path.basename(file_path).replace(".txt", "")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        # 自动添加段首缩进（每段缩进2字符）
        content = re.sub(r'<p>(?!\s)', '<p style="text-indent: 2em;">', content)
        chapters.append({
            "title": chapter_title,
            "content": content,
            "file_name": f"chap_{idx+1}.xhtml"
        })
    return chapters

def generate_epub():
    """生成EPUB核心函数"""
    # 1. 创建书籍对象
    book = epub.EpubBook()
    book.set_identifier(f"id_{BOOK_TITLE}")  # 唯一标识
    book.set_title(BOOK_TITLE)
    book.set_language("zh")
    book.add_author(AUTHOR)

    # 2. 添加封面
    cover_path = find_cover_image()
    if cover_path:
        with open(cover_path, "rb") as f:
            book.set_cover("cover.jpg", f.read())

    # 3. 定义CSS样式（含段首缩进）
    css_content = '''
    p { 
        text-indent: 2em;  /* 段首缩进 */
        margin-top: 0;
        margin-bottom: 1em;
        text-align: justify;
    }
    h1, h2, h3 { text-align: center; }
    '''
    style_item = epub.EpubItem(
        uid="style_default",
        file_name="style/main.css",
        media_type="text/css",
        content=css_content
    )
    book.add_item(style_item)

    # 4. 添加章节
    chapters = load_chapters()
    spine = ["nav"]  # 阅读顺序
    toc = []         # 目录结构
    for chap in chapters:
        # 创建章节HTML
        chapter_html = epub.EpubHtml(
            title=chap["title"],
            file_name=chap["file_name"],
            lang="zh"
        )
        chapter_html.content = f'''
        <html>
          <head><link rel="stylesheet" href="../style/main.css"/></head>
          <body>
            <h2>{chap["title"]}</h2>
            {chap["content"]}
          </body>
        </html>
        '''
        book.add_item(chapter_html)
        spine.append(chapter_html)
        toc.append(epub.Link(chap["file_name"], chap["title"], f"chap_{len(toc)+1}"))

    # 5. 设置书籍结构
    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNav())
    book.add_item(epub.EpubNcx())

    # 6. 保存文件
    output_path = os.path.join(os.path.dirname(CHAPTERS_DIR), f"{BOOK_TITLE}.epub")
    epub.write_epub(output_path, book, {})
    print(f"✅ 付费下载为盗版，免费EPUB生成成功！路径：{output_path}")

if __name__ == "__main__":
    generate_epub()