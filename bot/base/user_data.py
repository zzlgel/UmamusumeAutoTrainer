import os

base_path = "userdata"


def write_file(filename, content):
    filepath = os.path.dirname(base_path + filename)
    # 如果文件夹不存在则创建文件
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    # 使用with关键字来正确管理文件资源，确保在不再需要文件后正确关闭文件
    with open(base_path + filename, 'w', encoding='utf-8') as f:
        f.write(content)
