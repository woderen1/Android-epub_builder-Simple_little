import os #自用脚本，只用了python标准库，暴力删除txt文件的前11行和倒数第1行和把 （插图00x） 暴力替换为 [00x.jpg]
import re

# 设置工作目录
work_dir = "/storage/emulated/0/Download/1DMP/lk1novel/"
# 创建输出目录
output_dir = os.path.join(work_dir, "otxt")
os.makedirs(output_dir, exist_ok=True)

# 处理单个文件函数
def process_file(file_path, output_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 删除前11行和最后1行（保留第12行到倒数第2行）
    if len(lines) > 12:
        processed_lines = lines[11:-1]
    else:
        processed_lines = lines  # 对于行数不足的文件保持原样
    
    # 合并处理后的文本
    content = ''.join(processed_lines)
    
    # 替换插图格式
    pattern = re.compile(r'（插图(\d+)）')
    processed_content = pattern.sub(r'[\1.jpg]', content)
    
    # 写入输出文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(processed_content)

# 遍历工作目录下的txt文件
for filename in os.listdir(work_dir):
    if filename.endswith(".txt"):
        input_path = os.path.join(work_dir, filename)
        output_path = os.path.join(output_dir, filename)
        
        print(f"处理中: {filename}")
        try:
            process_file(input_path, output_path)
        except Exception as e:
            print(f"处理 {filename} 时出错: {str(e)}")
            continue

print("处理完成！输出文件保存在 otxt 文件夹")
