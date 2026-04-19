#!/usr/bin/env python3
"""
Swap ## さらに学ぶためのリソース and ## AIへの詠唱例 blocks
so that AI詠唱例 comes before さらに学ぶ.
"""
import re
import glob
import sys

def swap_sections(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    has_learn = '## さらに学ぶためのリソース' in content
    has_ai = '## AIへの詠唱例' in content

    if not has_learn or not has_ai:
        return False

    learn_pos = content.find('## さらに学ぶためのリソース')
    ai_pos = content.find('## AIへの詠唱例')

    # Only swap if さらに学ぶ comes BEFORE AI詠唱例
    if learn_pos >= ai_pos:
        return False

    # Extract blocks: from heading to just before next ## heading or EOF
    pattern_learn = r'(## さらに学ぶためのリソース.*?)(?=\n## |\Z)'
    pattern_ai = r'(## AIへの詠唱例.*?)(?=\n## |\Z)'

    learn_match = re.search(pattern_learn, content, re.DOTALL)
    ai_match = re.search(pattern_ai, content, re.DOTALL)

    if not learn_match or not ai_match:
        return False

    learn_block = learn_match.group(1)
    ai_block = ai_match.group(1)

    placeholder = "\x00LEARN_PLACEHOLDER\x00"
    new_content = content.replace(learn_block, placeholder, 1)
    new_content = new_content.replace(ai_block, learn_block, 1)
    new_content = new_content.replace(placeholder, ai_block, 1)

    if new_content == content:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True


if __name__ == '__main__':
    pattern = sys.argv[1] if len(sys.argv) > 1 else 'chapters/**/*.md'
    files = glob.glob(pattern, recursive=True)
    swapped = []
    for f in sorted(files):
        if swap_sections(f):
            swapped.append(f)

    print(f"Swapped {len(swapped)} files:")
    for f in swapped:
        print(f"  {f}")
