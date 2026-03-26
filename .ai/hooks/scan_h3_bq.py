#!/usr/bin/env python3
import re, glob, sys

def check_h3_density(content):
    results = []
    parts = re.split(r'(?=^## )', content, flags=re.MULTILINE)
    for part in parts:
        h2m = re.match(r'^## (.+)', part)
        if not h2m:
            continue
        h3_count = len(re.findall(r'^### ', part, re.MULTILINE))
        if h3_count > 5:
            results.append((h2m.group(1)[:40], h3_count))
    return results

def check_blockquotes(content):
    results = []
    current = 0
    start = 0
    for i, line in enumerate(content.split('\n')):
        if line.startswith('> '):
            if current == 0:
                start = i
            current += 1
        else:
            if current >= 15:
                results.append((start+1, current))
            current = 0
    if current >= 15:
        results.append((start+1, current))
    return results

files = sorted(glob.glob('chapters/**/*.md', recursive=True))
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    h3i = check_h3_density(content)
    bqi = check_blockquotes(content)
    if h3i or bqi:
        short = f.replace('chapters\\', 'ch/').replace('chapters/', 'ch/')
        sys.stdout.buffer.write(f"{short}:\n".encode('utf-8'))
        for sec, cnt in h3i:
            sys.stdout.buffer.write(f"  H3={cnt} in '{sec}'\n".encode('utf-8'))
        for line, cnt in bqi:
            sys.stdout.buffer.write(f"  BlockQuote={cnt} lines (at line {line})\n".encode('utf-8'))
