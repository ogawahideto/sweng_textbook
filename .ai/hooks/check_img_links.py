import re, os, glob

broken = []
total = 0
for md in glob.glob('chapters/**/*.md', recursive=True):
    d = os.path.dirname(md)
    with open(md, encoding='utf-8') as f:
        txt = f.read()
    for m in re.finditer(r'!\[[^\]]*\]\(([^)]+)\)', txt):
        p = m.group(1)
        if p.startswith('http'):
            continue
        total += 1
        full = os.path.normpath(os.path.join(d, p))
        if not os.path.exists(full):
            broken.append((md.replace(os.sep, '/'), p))

print("checked image refs:", total, "/ broken:", len(broken))
for md, p in broken:
    print("  BROKEN:", md, "->", p)
