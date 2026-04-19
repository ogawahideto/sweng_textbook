#!/usr/bin/env python3
import re, glob, sys

def check_figure_context(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    issues = []
    for i, line in enumerate(lines):
        if not line.startswith('!['):
            continue
        before = lines[i-1].strip() if i > 0 else ''
        after = lines[i+1].strip() if i < len(lines)-1 else ''

        no_intro = before in ('', '---') or before.startswith('#') or before.startswith('|')
        no_followup = after in ('', '---') or after.startswith('#') or after.startswith('|') or after.startswith('-') or after.startswith('*')

        if no_intro or no_followup:
            tag = []
            if no_intro: tag.append('no-intro')
            if no_followup: tag.append('no-followup')
            issues.append((i+1, ','.join(tag)))
    return issues

files = sorted(glob.glob('chapters/**/*.md', recursive=True))
total = 0
for f in files:
    issues = check_figure_context(f)
    if issues:
        short = f.replace('chapters\\', 'ch/').replace('chapters/', 'ch/')
        sys.stdout.buffer.write(f"{short}: {len(issues)} figs\n".encode('utf-8'))
        for line, tag in issues[:3]:
            sys.stdout.buffer.write(f"  line {line}: {tag}\n".encode('utf-8'))
        total += len(issues)
sys.stdout.buffer.write(f"\nTotal: {total} figures missing context\n".encode('utf-8'))
