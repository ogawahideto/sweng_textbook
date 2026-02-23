import os
import re

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

def normalize_paths(content):
    # すべての ../assets/ または ../../../assets/ を assets/ に統一
    pattern = r'\.\.\/+(assets\/)'
    return re.sub(pattern, r'\1', content)

output_file = 'full_book.md'

with open(output_file, 'w', encoding='utf-8') as outfile:
    for entry in entries:
        if not os.path.exists(entry):
            print(f"Warning: {entry} not found.")
            continue
            
        with open(entry, 'r', encoding='utf-8') as infile:
            content = infile.read()
            # パスの正規化
            content = normalize_paths(content)
            # 境界を挿入
            outfile.write(f"\n\n<!-- SECTION_START: {entry} -->\n\n")
            outfile.write(content)
            outfile.write("\n\n")

print(f"Successfully integrated all files into {output_file}")
