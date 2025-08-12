#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import uuid
import zipfile
import shutil
import sys  # 新增导入sys模块
from datetime import datetime

# =============== 用户配置区域 (按需修改) ===============
WORK_DIR = "/storage/emulated/0/Download/Exzbook/"
BOOK_TITLE = "电子书名"
BOOK_AUTHOR = "默认作者"
BOOK_LANG = "zh-CN"
PUBLISHER = "P默认"
ISBN = "none"
# ==================================================

def main():
    try:
        print("="*50)
        print(f"开始生成EPUB: {BOOK_TITLE}")
        print("="*50)
        
        # 清理旧临时文件
        print("[1/8] 清理旧临时文件...")
        temp_dir = os.path.join(WORK_DIR, "temp_epub")
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        # 准备目录结构
        print("[2/8] 准备目录结构...")
        oebps_dir = os.path.join(WORK_DIR, "OEBPS")
        os.makedirs(temp_dir, exist_ok=True)
        epub_dir = os.path.join(temp_dir, "OEBPS")
        os.makedirs(epub_dir, exist_ok=True)
        
        # 创建必需目录
        os.makedirs(os.path.join(epub_dir, "styles"), exist_ok=True)
        os.makedirs(os.path.join(epub_dir, "images"), exist_ok=True)
        
        # 1. 转换文本文件为XHTML
        print("[3/8] 转换文本章节为XHTML...")
        chapters = convert_txt_to_xhtml(oebps_dir, epub_dir)
        print(f"  转换完成: 共 {len(chapters)} 个章节")
        
        # 2. 拷贝图片
        print("[4/8] 处理图片资源...")
        cover_image = copy_images(os.path.join(oebps_dir, "images"), os.path.join(epub_dir, "images"))
        if cover_image:
            print(f"  封面图片: {cover_image}")
        else:
            print("  未找到封面图片，将使用文本封面")
        
        # 3. 生成必要文件
        print("[5/8] 生成电子书组件...")
        gen_css_file(epub_dir)
        gen_nav_file(epub_dir, chapters)
        gen_toc_ncx(epub_dir, BOOK_TITLE, chapters)
        gen_cover(epub_dir, cover_image)
        gen_package_opf(epub_dir, BOOK_TITLE, BOOK_AUTHOR, BOOK_LANG, PUBLISHER, ISBN, chapters, cover_image)
        gen_container_xml(temp_dir)
        gen_mimetype(temp_dir)
        print("  所有组件生成完成")
        
        # 4. 打包EPUB
        print("[6/8] 打包EPUB文件...")
        output_path = os.path.join(WORK_DIR, f"{BOOK_TITLE}.epub")
        create_epub(temp_dir, output_path)
        
        # 5. 清理临时文件
        print("[7/8] 清理临时文件...")
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print("[8/8] 完成!")
        print("="*50)
        print(f"EPUB生成成功: {output_path}")
        print(f"文件大小: {os.path.getsize(output_path)//1024} KB")
        print("="*50)
    
    except Exception as e:
        # 错误处理
        print("\n" + "!"*50)
        print("生成EPUB时出错!")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print("!"*50)
        
        # 尝试清理临时文件
        print("\n正在清理临时文件...")
        temp_dir = os.path.join(WORK_DIR, "temp_epub")
        shutil.rmtree(temp_dir, ignore_errors=True)
        print("临时文件已清理")
        
        sys.exit(1)  # 退出并返回错误代码

def convert_txt_to_xhtml(src_dir, dest_dir):
    """转换TXT文件为XHTML格式，处理图片引用"""
    chapter_files = sorted([f for f in os.listdir(src_dir) if f.endswith(".txt") and re.match(r'^\d+', f)])
    chapters = []
    
    for filename in chapter_files:
        # 处理文件名（保留自然语言后缀）
        basename = os.path.splitext(filename)[0]
        xhtml_name = f"{basename}.xhtml"
        title = re.sub(r'^\d+', '', basename).strip()
        
        with open(os.path.join(src_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
            
             # +++ 添加章节转换提示 +++
        print(f"  转换章节: {filename} -> {xhtml_name} (标题: '{title}')")
        # +++++++++++++++++++++++
        
        with open(os.path.join(src_dir, filename), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 处理图片引用 [image.jpg]
        content = re.sub(
            r'\[([^\]]+\.(?:jpg|png))\]', 
            r'<img class="illustration" src="images/\1" alt="插图"/>', 
            content
        )
        
        # 包裹段落
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        wrapped_content = '\n'.join([f'    <p>{p}</p>' for p in paragraphs])
        
        # 生成XHTML
        with open(os.path.join(dest_dir, xhtml_name), 'w', encoding='utf-8') as f:
            f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="styles/main.css"/>
</head>
<body>
    <h1>{title}</h1>
{wrapped_content}
</body>
</html>''')
        
        chapters.append({
            'id': f'ch{len(chapters)+1}',
            'title': title,
            'filename': xhtml_name
        })
    
    return chapters

def copy_images(src_img_dir, dest_img_dir):
    """拷贝图片文件并返回封面图片路径"""
    if not os.path.exists(src_img_dir):
        return None
    
    cover_image = None
    for filename in os.listdir(src_img_dir):
        if not filename.endswith(('.jpg', '.png')):
            continue
            
        src = os.path.join(src_img_dir, filename)
        dst = os.path.join(dest_img_dir, filename)
        shutil.copy2(src, dst)
        
        # 检查封面
        if filename.lower().startswith('cover'):
            cover_image = os.path.join('images', filename)
    
    return cover_image

def gen_css_file(epub_dir):
    """生成CSS样式文件"""
    css_path = os.path.join(epub_dir, "styles", "main.css")
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write('''/* 基础排版样式 */
p {
    text-indent: 2em;
    margin: 0 0 1em 0;
    text-align: justify;
    line-height: 1.6;
}

/* 标题样式 */
h1, h2 {
    text-align: center;
    page-break-after: avoid;
    margin-top: 2em;
}

/* 图片样式 */
img.illustration {
    display: block;
    max-width: 90%;
    margin: 1em auto;
    text-align: center;
}

/* 封面样式 */
#cover {
    text-align: center;
    page-break-after: always;
}

#cover img {
    height: 95vh;
    max-width: 100%;
}''')

def gen_nav_file(epub_dir, chapters):
    """生成导航文件 nav.xhtml"""
    with open(os.path.join(epub_dir, "nav.xhtml"), 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>目录</title>
    <meta charset="utf-8"/>
</head>
<body>
    <nav epub:type="toc">
        <h1>目录</h1>
        <ol>
            <li><a href="cover.xhtml">封面</a></li>''')
        
        for ch in chapters:
            f.write(f'            <li><a href="{ch["filename"]}">{ch["title"]}</a></li>\n')
        
        f.write('''        </ol>
    </nav>
</body>
</html>''')

def gen_toc_ncx(epub_dir, book_title, chapters):
    """生成NCX目录"""
    with open(os.path.join(epub_dir, "toc.ncx"), 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
    <head>
        <meta name="dtb:uid" content="urn:uuid:{str(uuid.uuid4())}"/>
        <meta name="dtb:depth" content="1"/>
        <meta name="dtb:totalPageCount" content="0"/>
        <meta name="dtb:maxPageNumber" content="0"/>
    </head>
    <docTitle><text>{book_title}</text></docTitle>
    <navMap>
        <navPoint id="cover" playOrder="1">
            <navLabel><text>封面</text></navLabel>
            <content src="cover.xhtml"/>
        </navPoint>''')
        
        for i, ch in enumerate(chapters):
            f.write(f'''
        <navPoint id="{ch["id"]}" playOrder="{i+2}">
            <navLabel><text>{ch["title"]}</text></navLabel>
            <content src="{ch["filename"]}"/>
        </navPoint>''')
        
        f.write('''
    </navMap>
</ncx>''')

def gen_cover(epub_dir, cover_image):
    """生成封面文件"""
    cover_content = '''<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <title>封面</title>
    <link rel="stylesheet" type="text/css" href="styles/main.css"/>
</head>
<body>
    <div id="cover">
        <h1>{title}</h1>
        <h2>{author}</h2>'''.format(title=BOOK_TITLE, author=BOOK_AUTHOR)
    
    if cover_image:
        cover_content += f'\n        <img src="{cover_image}" alt="封面"/>'
    
    cover_content += '''
    </div>
</body>
</html>'''
    
    with open(os.path.join(epub_dir, "cover.xhtml"), 'w', encoding='utf-8') as f:
        f.write(cover_content)

def gen_package_opf(epub_dir, title, author, lang, publisher, isbn, chapters, cover_image):
    """生成package.opf文件"""
    now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    
    with open(os.path.join(epub_dir, "package.opf"), 'w', encoding='utf-8') as f:
        f.write(f'''<?xml version="1.0" encoding="UTF-8"?>
<package version="3.0" 
        xmlns="http://www.idpf.org/2007/opf"
        unique-identifier="book-id">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
        <dc:identifier id="book-id">urn:uuid:{str(uuid.uuid4())}</dc:identifier>
        <dc:title>{title}</dc:title>
        <dc:creator>{author}</dc:creator>
        <dc:language>{lang}</dc:language>
        <dc:publisher>{publisher}</dc:publisher>
        <dc:identifier>{isbn}</dc:identifier>
        <meta property="dcterms:modified">{now}</meta>''')
        
        if cover_image:
            cover_filename = os.path.basename(cover_image)
            cover_type = "image/jpeg" if cover_filename.lower().endswith('.jpg') else "image/png"
            f.write(f'''
        <meta name="cover" content="cover-img"/>
        <meta property="rendition:layout">pre-paginated</meta>''')
        
        f.write('''
    </metadata>
    <manifest>
        <item id="nav" href="nav.xhtml" properties="nav" media-type="application/xhtml+xml"/>
        <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
        <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>''')
        
        for ch in chapters:
            f.write(f'''
        <item id="{ch["id"]}" href="{ch["filename"]}" media-type="application/xhtml+xml"/>''')
        
        f.write('''
        <item id="main-css" href="styles/main.css" media-type="text/css"/>''')
        
        if cover_image:
            cover_filename = os.path.basename(cover_image)
            cover_type = "image/jpeg" if cover_filename.lower().endswith('.jpg') else "image/png"
            f.write(f'''
        <item id="cover-img" href="{cover_image}" media-type="{cover_type}" properties="cover-image"/>''')
        
        # 添加图片资源
        images_dir = os.path.join(epub_dir, "images")
        if os.path.exists(images_dir):
            for img in os.listdir(images_dir):
                img_type = "image/jpeg" if img.lower().endswith('.jpg') else "image/png"
                f.write(f'''
        <item id="img-{img.split(".")[0]}" href="images/{img}" media-type="{img_type}"/>''')
        
        f.write('''
    </manifest>
    <spine toc="ncx">
        <itemref idref="cover"/>''')
        
        for ch in chapters:
            f.write(f'''
        <itemref idref="{ch["id"]}"/>''')
        
        f.write('''
    </spine>
    <guide>
        <reference type="cover" title="封面" href="cover.xhtml"/>
    </guide>
</package>''')

def gen_container_xml(temp_dir):
    """生成container.xml"""
    meta_inf_dir = os.path.join(temp_dir, "META-INF")
    os.makedirs(meta_inf_dir, exist_ok=True)
    
    with open(os.path.join(meta_inf_dir, "container.xml"), 'w', encoding='utf-8') as f:
        f.write('''<?xml version="1.0"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>''')

def gen_mimetype(temp_dir):
    """生成mimetype文件"""
    with open(os.path.join(temp_dir, "mimetype"), 'w', encoding='utf-8') as f:
        f.write('application/epub+zip')

def create_epub(temp_dir, output_path):
    """创建EPUB压缩文件"""
    with zipfile.ZipFile(output_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # 单独处理mimetype文件（不能压缩）
        mimetype_path = os.path.join(temp_dir, "mimetype")
        zf.write(mimetype_path, "mimetype", compress_type=zipfile.ZIP_STORED)
        
        # 添加其他文件（需要压缩）
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                if file == "mimetype":
                    continue
                
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, temp_dir)
                zf.write(full_path, rel_path)

if __name__ == "__main__":
    main()
