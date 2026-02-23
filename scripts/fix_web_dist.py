import os
import re

dist_dir = 'dist'

# 構成ファイルのリスト
entries = [
    'COVER.md',
    'toc.md',
    'chapters/prologue/prologue.md',
    'chapters/part1/chapter01/chapter01.md',
    'chapters/part1/chapter01/1-1.md',
    'chapters/part1/chapter01/1-2.md',
    'chapters/part1/chapter01/1-3.md',
    'chapters/part1/chapter01/1-4.md',
    'chapters/part1/chapter01/1-5.md',
    'chapters/part1/chapter02/chapter02.md',
    'chapters/part1/chapter02/2-1.md',
    'chapters/part1/chapter02/2-2.md',
    'chapters/part1/chapter02/2-3.md',
    'chapters/part1/chapter02/2-4.md',
    'chapters/part1/chapter02/2-5.md',
    'chapters/part1/chapter02/2-6.md',
    'chapters/part2/chapter03/chapter03.md',
    'chapters/part2/chapter03/3-1.md',
    'chapters/part2/chapter03/3-2.md',
    'chapters/part2/chapter03/3-3.md',
    'chapters/part2/chapter03/3-4.md',
    'chapters/part2/chapter03/3-5.md',
    'chapters/part2/chapter03/3-6.md',
    'chapters/part2/chapter03/3-7.md',
    'chapters/part2/chapter03/3-8.md',
    'chapters/part2/chapter04/chapter04.md',
    'chapters/part2/chapter04/4-1.md',
    'chapters/part2/chapter04/4-2.md',
    'chapters/part2/chapter04/4-3.md',
    'chapters/part2/chapter04/4-4.md',
    'chapters/part2/chapter04/4-5.md',
    'chapters/part2/chapter04/4-6.md',
    'chapters/part3/chapter05/chapter05.md',
    'chapters/part3/chapter05/5-1.md',
    'chapters/part3/chapter05/5-2.md',
    'chapters/part3/chapter05/5-3.md',
    'chapters/part3/chapter05/5-4.md',
    'chapters/part3/chapter06/chapter06.md',
    'chapters/part3/chapter06/6-1.md',
    'chapters/part3/chapter06/6-2.md',
    'chapters/part3/chapter06/6-3.md',
    'chapters/part3/chapter06/6-4.md',
    'chapters/part3/chapter06/6-5.md',
    'chapters/part3/chapter06/6-6.md',
    'chapters/part4/chapter07/chapter07.md',
    'chapters/part4/chapter07/7-1.md',
    'chapters/part4/chapter07/7-2.md',
    'chapters/part4/chapter07/7-3.md',
    'chapters/part4/chapter07/7-4.md',
    'chapters/part4/chapter08/chapter08.md',
    'chapters/part4/chapter08/8-1.md',
    'chapters/part4/chapter08/8-2.md',
    'chapters/part4/chapter08/8-3.md',
    'chapters/epilogue/epilogue.md',
]

html_files = [e.replace('.md', '.html') for e in entries]

def get_relative_url(current, target):
    if not target: return "#"
    curr_parts = current.split('/')
    target_parts = target.split('/')
    
    # 共通の親ディレクトリまで戻る
    depth = len(curr_parts) - 1
    prefix = '../' * depth
    return prefix + target

for i, html_file in enumerate(html_files):
    full_path = os.path.join(dist_dir, html_file)
    if not os.path.exists(full_path):
        continue

    # 元のファイルを読み込む（文字化け無視して構造だけ取る）
    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
        html_content = f.read()

    # Markdownから正しいタイトルを取得
    md_path = entries[i]
    title = "デジタル・アルケミー"
    with open(md_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        if first_line.startswith('# '):
            title = first_line.replace('# ', '').strip()

    # ナビゲーションのURL計算
    prev_url = get_relative_url(html_file, html_files[i-1]) if i > 0 else None
    next_url = get_relative_url(html_file, html_files[i+1]) if i < len(html_files)-1 else None
    toc_url = get_relative_url(html_file, "toc.html")

    prev_link = f'<a href="{prev_url}" style="color: #1E88E5; text-decoration: none;">← 前へ</a>' if prev_url else '<span></span>'
    next_link = f'<a href="{next_url}" style="color: #1E88E5; text-decoration: none;">次へ →</a>' if next_url else '<span></span>'
    toc_link = f'<a href="{toc_url}" style="color: #666; text-decoration: none; font-weight: bold;">目次</a>'

    nav_html = f'''
    <nav style="display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #ddd; font-family: sans-serif; position: sticky; top: 0; z-index: 1000;">
        {prev_link}
        {toc_link}
        {next_link}
    </nav>
    '''

    # 文字化け対策: ヘッダー部分をクリーンなものに置換
    # 既存の <head>...<body...> を正規化
    head_html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>{title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="{get_relative_url(html_file, "assets/styles/print.css")}">
    <style>
        body {{ max-width: 900px; margin: 0 auto; background: white; }}
        section {{ padding: 20px; }}
        img {{ max-width: 100%; height: auto; }}
    </style>
</head>
<body style="margin:0; padding:0;">
'''
    
    # 既存のコンテンツからボディ部分を抽出
    body_match = re.search(r'<body[^>]*>(.*)</body>', html_content, re.DOTALL)
    if body_match:
        inner_content = body_match.group(1)
        # 以前追加した不正なナビを削除
        inner_content = re.sub(r'<nav.*?</nav>', '', inner_content, flags=re.DOTALL)
        
        # リンクの .md -> .html 置換
        inner_content = inner_content.replace('.md"', '.html"').replace('.md#', '.html#')
        
        new_html = head_html + nav_html + '<main>' + inner_content + '</main>' + nav_html + '</body></html>'
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(new_html)

# index.html の更新
index_path = os.path.join(dist_dir, 'index.html')
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <title>デジタル・アルケミー 案内板</title>
    <style>
        body {{ font-family: sans-serif; text-align: center; padding: 100px 20px; background: #fafafa; color: #333; }}
        .card {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }}
        h1 {{ color: #1E88E5; margin-bottom: 10px; }}
        .btn {{ display: inline-block; margin-top: 30px; padding: 15px 40px; background: #1E88E5; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 1.2em; transition: background 0.3s; }}
        .btn:hover {{ background: #1565C0; }}
        .toc-link {{ display: block; margin-top: 20px; color: #666; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>『「楽しい」ソフトウェア工学の教科書』</h1>
        <p>デジタル・アルケミー：伝統の美学とAIで紡ぐ創造の地図</p>
        <a href="COVER.html" class="btn">本を開く</a>
        <a href="toc.html" class="toc-link">目次を見る</a>
    </div>
</body>
</html>
''')

print("Web distribution fixed with clean headers and correct relative links.")
