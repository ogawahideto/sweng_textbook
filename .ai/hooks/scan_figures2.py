#!/usr/bin/env python3
"""改良版: 空行をスキップして前後のコンテキストをチェック"""
import re, glob, sys

def check_figure_context(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines):
        if not line.startswith('!['):
            continue

        # 直前の非空行を探す（最大3行前まで）
        before = ''
        for j in range(i-1, max(i-4, -1), -1):
            s = lines[j].strip()
            if s:
                before = s
                break

        # 直後の非空行を探す（最大3行後まで）
        after = ''
        for j in range(i+1, min(i+4, len(lines))):
            s = lines[j].strip()
            if s:
                after = s
                break

        no_intro = not before or before == '---' or before.startswith('#') or before.startswith('|')
        no_followup = not after or after == '---' or after.startswith('#') or after.startswith('|') or after.startswith('-') or after.startswith('*')

        if no_intro or no_followup:
            tag = []
            if no_intro: tag.append('no-intro')
            if no_followup: tag.append('no-followup')
            issues.append((i+1, ','.join(tag), before[:50], after[:50]))
    return issues

files = sorted(glob.glob('chapters/**/*.md', recursive=True))
total = 0
for f in files:
    issues = check_figure_context(f)
    if issues:
        short = f.replace('chapters\\\\', 'ch/').replace('chapters/', 'ch/')
        sys.stdout.buffer.write(f"{short}: {len(issues)} figs\n".encode('utf-8'))
        for lineno, tag, bef, aft in issues[:5]:
            sys.stdout.buffer.write(f"  line {lineno}: [{tag}]\n".encode('utf-8'))
            sys.stdout.buffer.write(f"    before: {bef!r}\n".encode('utf-8'))
            sys.stdout.buffer.write(f"    after:  {aft!r}\n".encode('utf-8'))
        total += len(issues)
sys.stdout.buffer.write(f"\nTotal真の違反: {total}\n".encode('utf-8'))
