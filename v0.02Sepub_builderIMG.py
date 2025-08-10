#!/data/data/com.termux/files/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re
import zipfile
import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom

# =====================================================================
# 用户配置区域 - 请根据实际情况修改以下参数
# =====================================================================

# 工作目录（Termux中的绝对路径）
WORK_DIR = "/storage/emulated/0/Download/Ezbook/"

# 书籍元数据
BOOK_METADATA = {
    "title": "魅魔の记录",      # 书名
    "author": "L魅魔！",           # 作者
    "language": "zh-CN",        # 语言代码
    "publisher": "魅魔出版",    # 出版社
    "isbn": "",  # ISBN号
    "uid": "urn:uuid:12345678-90ab-cdef-1234-567890abcdef"  # 唯一标识符
}

# =====================================================================
# 主处理脚本（无需修改以下代码）
# =====================================================================

def main():
    try:
        print("📖 魅魔开始写书")
        print(f"📂 魅魔工作的地方: {WORK_DIR}")
        
        # 检查工作目录
        oebps_dir = os.path.join(WORK_DIR, "OEBPS")
        images_dir = os.path.join(oebps_dir, "images")
        
        if not os.path.exists(oebps_dir):
            print("❌ 错误: OEBPS目录不存在")
            return
        
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
            print("🖼️ 魅魔创建images目录")
        
        # 1. 处理文本文件
        print("⏳ 魅魔正在处理文本...")
        txt_files = find_and_convert_txt(oebps_dir)
        
        # 2. 创建核心文件
        print("⚙️ 魅魔正在召唤配置文件...")
        create_content_opf(oebps_dir, txt_files)
        create_toc_files(oebps_dir, txt_files)
        create_cover_page(oebps_dir)
        create_container_files(WORK_DIR)
        
        # 3. 打包EPUB
        epub_path = os.path.join(WORK_DIR, f"{BOOK_METADATA['title']}.epub")
        package_epub(WORK_DIR, epub_path)
        
        print(f"\n✅ 魅魔写好书了! 路径: {epub_path}")
        print(f"📚 书籍信息: 《{BOOK_METADATA['title']}》- {BOOK_METADATA['author']}")
        
    except Exception as e:
        print(f"\n❌ 魅魔发现了错误: {str(e)}")
        print("⚠️ 请检查: 1) 文件路径 2) 文本编码 3) 图片文件名")

def find_and_convert_txt(oebps_dir):
    """查找并转换TXT文件为XHTML"""
    txt_files = []
    
    for fname in os.listdir(oebps_dir):
        if not fname.endswith('.txt'):
            continue
            
        print(f"  处理文件: {fname}")
        base_name = os.path.splitext(fname)[0]
        xhtml_name = f"{base_name}.xhtml"
        
        # 读取并转换内容
        txt_path = os.path.join(oebps_dir, fname)
        with open(txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        content = convert_txt_to_xhtml(content)
        
        # 保存为XHTML
        xhtml_path = os.path.join(oebps_dir, xhtml_name)
        with open(xhtml_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 添加到文件列表
        txt_files.append({
            "base": base_name,
            "xhtml": xhtml_name,
            "number": extract_number(base_name),
            "title": extract_title(base_name)
        })
    
    # 按数字排序
    txt_files.sort(key=lambda x: x["number"])
    return txt_files

def convert_txt_to_xhtml(content):
    """转换纯文本到XHTML格式"""
    # 删除所有空行
    lines = [line for line in content.splitlines() if line.strip()]
    
    # 转换图片引用
    processed = []
    for line in lines:
        img_match = re.match(r'^\[([^\]]+\.(jpg|png))\]$', line.strip())
        if img_match:
            img_file = img_match.group(1)
            line = f'    <div><img src="images/{img_file}" alt="插图"/></div>'
        else:
            line = f'    <p>{line}</p>'
        processed.append(line)
    
    # 包装为完整XHTML
    xhtml_content = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>内容页</title>
    <link href="styles/main.css" rel="stylesheet" type="text/css"/>
</head>
<body>
{}
</body>
</html>'''.format('\n'.join(processed))
    
    return xhtml_content

def extract_number(filename):
    """提取文件名中的数字部分"""
    number_part = ''.join(filter(str.isdigit, filename))
    return int(number_part) if number_part else 0

def extract_title(filename):
    """提取文件名中的文字部分"""
    return re.sub(r'^\d+', '', filename).strip()

def create_content_opf(oebps_dir, chapters):
    """创建content.opf文件"""
    # 创建根元素
    package = ET.Element('package', {
        "xmlns": "http://www.idpf.org/2007/opf",
        "version": "3.0",
        "unique-identifier": "uid"
    })
    
    # 元数据部分
    metadata = ET.SubElement(package, 'metadata', {
        "xmlns:dc": "http://purl.org/dc/elements/1.1/"
    })
    
    ET.SubElement(metadata, 'dc:title').text = BOOK_METADATA['title']
    ET.SubElement(metadata, 'dc:creator').text = BOOK_METADATA['author']
    ET.SubElement(metadata, 'dc:language').text = BOOK_METADATA['language']
    ET.SubElement(metadata, 'dc:publisher').text = BOOK_METADATA['publisher']
    ET.SubElement(metadata, 'dc:identifier', {"id": "uid"}).text = BOOK_METADATA['uid']
    ET.SubElement(metadata, 'meta', {"property": "dcterms:modified"}).text = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    ET.SubElement(metadata, 'meta', {"name": "cover", "content": "cover-img"})
    
    # 清单部分
    manifest = ET.SubElement(package, 'manifest')
    
    # 添加CSS文件
    ET.SubElement(manifest, 'item', {
        "id": "main-css",
        "href": "styles/main.css",
        "media-type": "text/css"
    })
    
    # 添加封面图片
    cover_img = find_cover_image(oebps_dir)
    if cover_img:
        img_type = "image/jpeg" if cover_img.endswith('.jpg') else "image/png"
        ET.SubElement(manifest, 'item', {
            "id": "cover-img",
            "href": f"images/{cover_img}",
            "media-type": img_type
        })
    
    # 添加封面页面
    ET.SubElement(manifest, 'item', {
        "id": "cover",
        "href": "cover.xhtml",
        "media-type": "application/xhtml+xml"
    })
    
    # 添加章节文件
    for chap in chapters:
        ET.SubElement(manifest, 'item', {
            "id": chap["base"],
            "href": chap["xhtml"],
            "media-type": "application/xhtml+xml"
        })
    
    # 目录文件 (EPUB 2和EPUB 3)
    ET.SubElement(manifest, 'item', {
        "id": "toc",
        "href": "toc.xhtml",
        "media-type": "application/xhtml+xml",
        "properties": "nav"
    })
    ET.SubElement(manifest, 'item', {
        "id": "ncx",
        "href": "toc.ncx",
        "media-type": "application/x-dtbncx+xml"
    })
    
    # 目录结构
    spine = ET.SubElement(package, 'spine')
    spine.set('page-progression-direction', 'ltr')
    
    # 封面页
    ET.SubElement(spine, 'itemref', {"idref": "cover"})
    
    # 各章节
    for chap in chapters:
        ET.SubElement(spine, 'itemref', {"idref": chap["base"]})
    
    # 创建并保存文件
    xml_str = minidom.parseString(ET.tostring(package)).toprettyxml()
    opf_path = os.path.join(oebps_dir, 'content.opf')
    with open(opf_path, 'w', encoding='utf-8') as f:
        f.write(xml_str)

def find_cover_image(oebps_dir):
    """查找封面图片"""
    images_dir = os.path.join(oebps_dir, 'images')
    for f in os.listdir(images_dir):
        if re.match(r'cover\.(jpg|png)', f, re.IGNORECASE):
            return f
    return None

def create_toc_files(oebps_dir, chapters):
    """创建目录文件（EPUB2和EPUB3）"""
    # EPUB3目录 (toc.xhtml)
    toc_xhtml = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>目录</title>
</head>
<body>
    <nav epub:type="toc">
        <h1>目录</h1>
        <ol>
            <li><a href="cover.xhtml">封面</a></li>
            {}
        </ol>
    </nav>
</body>
</html>'''.format(
        '\n'.join([f'            <li><a href="{chap["xhtml"]}">{chap["title"] or "章节" + str(chap["number"])}</a></li>' 
                  for chap in chapters])
    )
    
    with open(os.path.join(oebps_dir, 'toc.xhtml'), 'w', encoding='utf-8') as f:
        f.write(toc_xhtml)
    
    # EPUB2目录 (toc.ncx)
    ncx = ET.Element('ncx', {
        "xmlns": "http://www.daisy.org/z3986/2005/ncx/",
        "version": "2005-1"
    })
    
    head = ET.SubElement(ncx, 'head')
    ET.SubElement(head, 'meta', {"name": "dtb:uid", "content": BOOK_METADATA['uid']})
    
    doc_title = ET.SubElement(ncx, 'docTitle')
    ET.SubElement(doc_title, 'text').text = BOOK_METADATA['title']
    
    nav_map = ET.SubElement(ncx, 'navMap')
    
    # 封面
    nav_point = ET.SubElement(nav_map, 'navPoint', {"id": "cover", "playOrder": "1"})
    nav_label = ET.SubElement(nav_point, 'navLabel')
    ET.SubElement(nav_label, 'text').text = "封面"
    ET.SubElement(nav_point, 'content', {"src": "cover.xhtml"})
    
    # 章节
    play_order = 2
    for chap in chapters:
        nav_point = ET.SubElement(nav_map, 'navPoint', {
            "id": f"nav-{chap['number']}",
            "playOrder": str(play_order)
        })
        nav_label = ET.SubElement(nav_point, 'navLabel')
        ET.SubElement(nav_label, 'text').text = chap['title'] or f"章节 {chap['number']}"
        ET.SubElement(nav_point, 'content', {"src": chap['xhtml']})
        play_order += 1
    
    xml_str = minidom.parseString(ET.tostring(ncx)).toprettyxml()
    with open(os.path.join(oebps_dir, 'toc.ncx'), 'w', encoding='utf-8') as f:
        f.write(xml_str)

def create_cover_page(oebps_dir):
    """创建封面页"""
    cover_content = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">
<head>
    <title>封面</title>
    <meta charset="utf-8"/>
    <link href="styles/main.css" rel="stylesheet" type="text/css"/>
</head>
<body class="cover">
    <div class="cover-image">
        <img src="images/cover.jpg" alt="封面" epub:type="cover"/>
    </div>
</body>
</html>'''
    
    with open(os.path.join(oebps_dir, 'cover.xhtml'), 'w', encoding='utf-8') as f:
        f.write(cover_content)

def create_container_files(work_dir):
    """创建META-INF和mimetype文件"""
    # 创建META-INF目录
    meta_inf = os.path.join(work_dir, 'META-INF')
    os.makedirs(meta_inf, exist_ok=True)
    
    # container.xml
    container = '''<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    <rootfiles>
        <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
    </rootfiles>
</container>'''
    
    with open(os.path.join(meta_inf, 'container.xml'), 'w', encoding='utf-8') as f:
        f.write(container)
    
    # mimetype
    with open(os.path.join(work_dir, 'mimetype'), 'w') as f:
        f.write('application/epub+zip')

def package_epub(work_dir, output_path):
    """打包为EPUB文件"""
    # 创建ZIP文件（注意：mimetype必须作为第一个文件且不压缩）
    with zipfile.ZipFile(output_path, 'w') as zipf:
        # 1. 添加mimetype（无压缩）
        mimetype_path = os.path.join(work_dir, 'mimetype')
        if os.path.exists(mimetype_path):
            zipf.write(mimetype_path, 'mimetype', compress_type=zipfile.ZIP_STORED)
        
        # 2. 添加META-INF
        meta_inf = os.path.join(work_dir, 'META-INF')
        if os.path.exists(meta_inf):
            for root, dirs, files in os.walk(meta_inf):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, work_dir)
                    zipf.write(file_path, arcname)
        
        # 3. 添加OEBPS内容
        oebps_dir = os.path.join(work_dir, 'OEBPS')
        if os.path.exists(oebps_dir):
            for root, dirs, files in os.walk(oebps_dir):
                for file in files:
                    # 跳过TXT原始文件
                    if file.endswith('.txt'):
                        continue
                        
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, work_dir)
                    zipf.write(file_path, arcname)
    
    print(f"\n📦 魅魔工作完毕，魅魔小姐希望你没有被盗版骗付费下载: {output_path}")

if __name__ == "__main__":
    # 确保创建CSS文件
    oebps_dir = os.path.join(WORK_DIR, "OEBPS")
    css_dir = os.path.join(oebps_dir, "styles")
    os.makedirs(css_dir, exist_ok=True)
    
    css_content = '''/* 基础样式 */
body { font-family: serif; margin: 1em; }
.cover { text-align: center; }
.cover-image { max-height: 95vh; }
.cover-image img { max-height: 95vh; margin: 0 auto; }'''
    
    css_path = os.path.join(css_dir, "main.css")
    if not os.path.exists(css_path):
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css_content)
    
    main()
