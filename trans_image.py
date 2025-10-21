import shutil
import re
import os


def trans_image(name):
    post_dir = f'content/posts/{name}'
    index_path = os.path.join(post_dir, "index.md")
    os.makedirs(post_dir, exist_ok=True)

    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 匹配 Markdown 图片：![alt](path "title")
    pattern = re.compile(
        r'!\[(.*?)\]\(\s*["\']?(.+?\.(?:png|jpg|jpeg|gif|webp|bmp))["\']?\s*(?:\s+"[^"]*")?\)',
        re.IGNORECASE
    )

    matches = list(pattern.finditer(content))
    orig_paths = [m.group(2) for m in matches]

    # 记录：原始匹配到的路径 -> 目标（规范化后）的最终文件名（仅文件名，不含目录）
    final_name_map = {}

    def to_underscore_name(filename: str) -> str:
        # 把任意空白替换成单个下划线
        return re.sub(r'\s+', '_', filename)

    def ensure_unique(dest_path: str) -> str:
        """若目标已存在，则在文件名后追加 _1, _2 ... 直到不冲突"""
        if not os.path.exists(dest_path):
            return dest_path
        root, ext = os.path.splitext(dest_path)
        i = 1
        while True:
            candidate = f"{root}_{i}{ext}"
            if not os.path.exists(candidate):
                return candidate
            i += 1

    for p in orig_paths:
        base = os.path.basename(p)                  # 原始文件名（可能含空格）
        norm_base = to_underscore_name(base)        # 规范化后的文件名（空格->下划线）
        target = os.path.join(post_dir, norm_base)  # 期望落地到的路径（可能会重名）

        # 情况 A：你上一次已经复制到了文章目录里（带空格的旧名字）
        old_local = os.path.join(post_dir, base)

        if os.path.exists(old_local):
            # 需要把 old_local 重命名为 target（若冲突则加序号）
            final_path = target if not os.path.exists(
                target) else ensure_unique(target)
            if os.path.abspath(old_local) != os.path.abspath(final_path):
                os.rename(old_local, final_path)
                print("✅ 重命名:", old_local, "→", final_path)
            else:
                print("✅ 已规范:", final_path)
            final_name_map[p] = os.path.basename(final_path)
            continue

        # 情况 B：文章目录中还没有，就从来源复制过来（来源可能是绝对/相对路径）
        # 依次尝试：用户写的路径本身、以文章目录为相对基准的路径
        src_candidates = [p, os.path.join(post_dir, p)]
        src = next((c for c in src_candidates if os.path.exists(c)), None)

        if src:
            final_path = target if not os.path.exists(
                target) else ensure_unique(target)
            if os.path.abspath(src) != os.path.abspath(final_path):
                shutil.copy(src, final_path)
                print("✅ 复制并规范:", src, "→", final_path)
            else:
                print("✅ 已存在且规范:", final_path)
            final_name_map[p] = os.path.basename(final_path)
        else:
            print("⚠️ 文件不存在:", p)
            # 找不到源时，仍然将映射设为规范化后的文件名，保证 MD 链接被规范化
            final_name_map[p] = norm_base

    # 根据映射替换 Markdown：只保留文件名，且空格->下划线
    def repl(m):
        alt = m.group(1)
        p = m.group(2)
        final_base = final_name_map.get(p)
        if not final_base:
            # 极端 fallback（理论上不应发生）
            final_base = to_underscore_name(os.path.basename(p))
        return f"![{alt}]({final_base})"

    new_content = re.sub(pattern, repl, content)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(new_content)


if __name__ == '__main__':
    trans_image("verl框架GPRO调参GSM8K")
