import shutil
import re
import os


# 操作变量name
def trans_image(name):
    path = f'content/posts/{name}'
    with open(os.path.join(path, "index.md"), "r", encoding="utf-8") as f:
        content = f.read()

    # 提取所有路径
    paths = re.findall(r"!\[.*?\]\((.*?)\)", content)

    # 复制
    for p in paths:
        if '\\' in p:
            shutil.copy(p, path)
            print("work on: "+p)

    # 替换内容
    new_content = re.sub(
        r"!\[(.*?)\]\((.*?)\)",
        lambda m: f"![{m.group(1)}]({m.group(2).split('\\')[-1].split('/')[-1]})",
        content
    )
    with open(os.path.join(path, "index.md"), "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == '__main__':
    trans_image("9.15_记录")
