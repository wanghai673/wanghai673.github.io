import shutil
import re
import os


def trans_image(name):
    path = f'content/posts/{name}'
    index_path = os.path.join(path, "index.md")

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = re.compile(
        r'!\[(.*?)\]\(\s*["\']?(.+?\.(?:png|jpg|jpeg|gif|webp|bmp))["\']?\s*(?:\s+".*?")?\)',
        re.IGNORECASE
    )

    paths = [m.group(2) for m in pattern.finditer(content)]

    for p in paths:
        if os.path.exists(p):
            shutil.copy(p, path)
            print("✅ work on:", p)
        else:
            print("⚠️ 文件不存在:", p)

    # 替换路径为文件名
    new_content = re.sub(
        r'!\[(.*?)\]\(\s*["\']?(.+?\.(?:png|jpg|jpeg|gif|webp|bmp))["\']?\s*(?:\s+".*?")?\)',
        lambda m: f"![{m.group(1)}]({os.path.basename(m.group(2))})",
        content,
        flags=re.IGNORECASE
    )

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == '__main__':
    trans_image("verl框架GPRO调参GSM8K")
