"""
見出し直前の独立段落（接続文）を検出するスクリプト
"""
import sys
import re
import os

def find_transitions(filepath):
    with open(filepath, encoding='utf-8') as f:
        lines = f.readlines()

    results = []
    for i, line in enumerate(lines):
        if re.match(r'^#{1,4} ', line):
            # 直前が空行で、その前がテキスト段落かチェック
            if i >= 2 and lines[i-1].strip() == '':
                prev_text = lines[i-2].strip()
                if (prev_text and
                    not prev_text.startswith('#') and
                    not prev_text.startswith('-') and
                    not prev_text.startswith('|') and
                    not prev_text.startswith('>') and
                    not prev_text.startswith('```') and
                    not prev_text.startswith('![') and
                    not prev_text.startswith('---') and
                    not prev_text.startswith('*')):
                    # さらに前も空行かチェック（独立段落であることを確認）
                    if i >= 3 and lines[i-3].strip() == '':
                        # まとめ・AI詠唱例・さらに学ぶ への接続は除外
                        heading = line.strip()
                        if not re.search(r'まとめ|AIへの詠唱例|さらに学ぶ', heading):
                            results.append((i-1, prev_text, i, heading))
    return results

targets = sys.argv[1:]
for filepath in targets:
    results = find_transitions(filepath)
    if results:
        print(f"\n=== {os.path.basename(filepath)} ===")
        for (text_line, text, heading_line, heading) in results:
            print(f"  L{text_line+1}: {text[:90]}")
            print(f"  → {heading}")
