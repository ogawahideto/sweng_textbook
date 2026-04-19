#!/usr/bin/env python3
"""Scan chapters for book-polish rule violations."""
import re
import glob
import sys
import os

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # Rule 1: H3 density
    sections = re.split(r'\n## ', content)
    for sec in sections[1:]:
        h3s = re.findall(r'^### ', sec, re.MULTILINE)
        if len(h3s) > 5:
            title = sec.split('\n')[0][:40]
            issues.append(f"[1-H3] H3={len(h3s)} in ## {title}")

    # Rule 7: long blockquotes (15+ lines)
    blocks = re.findall(r'(?:^> .+\n)+', content, re.MULTILINE)
    for b in blocks:
        lines = b.strip().split('\n')
        if len(lines) >= 15:
            issues.append(f"[7-COL] blockquote={len(lines)} lines")

    # Rule 8: callback phrases
    callbacks = re.findall(r'^(?:前節で[はにもが]|ここまで[でに]|本節では|この節では).+', content, re.MULTILINE)
    if callbacks:
        issues.append(f"[8-CB] {len(callbacks)} callbacks")

    return issues


if __name__ == '__main__':
    pattern = sys.argv[1] if len(sys.argv) > 1 else 'chapters/**/*.md'
    files = sorted(glob.glob(pattern, recursive=True))
    total = 0
    for f in files:
        issues = check_file(f)
        if issues:
            short = f.replace('chapters\\', '').replace('chapters/', '')
            sys.stdout.buffer.write(f"{short}:\n".encode('utf-8'))
            for i in issues:
                sys.stdout.buffer.write(f"  {i}\n".encode('utf-8'))
            total += len(issues)

    sys.stdout.buffer.write(f"\nTotal: {total} violations\n".encode('utf-8'))
