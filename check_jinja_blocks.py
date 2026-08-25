import re, pathlib, sys
p = pathlib.Path('templates')
if not p.exists():
    print("No templates dir found")
    sys.exit(1)

patterns = {
  'block': (re.compile(r'{%\s*block\b'), re.compile(r'{%\s*endblock\b')),
  'if':    (re.compile(r'{%\s*if\b'),    re.compile(r'{%\s*endif\b')),
  'for':   (re.compile(r'{%\s*for\b'),   re.compile(r'{%\s*endfor\b')),
}

for fname in sorted(p.rglob('*.html')):
    text = fname.read_text(encoding='utf-8')
    problems = []
    for name,(open_re,close_re) in patterns.items():
        opens = len(open_re.findall(text))
        closes = len(close_re.findall(text))
        if opens != closes:
            problems.append(f"{name}: opens={opens} closes={closes}")
    if problems:
        print(f"{fname}: " + ", ".join(problems))
