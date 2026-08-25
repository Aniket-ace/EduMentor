# check_jinja_braces.py
import pathlib, sys

p = pathlib.Path('templates')
if not p.exists():
    print("No templates dir found")
    sys.exit(1)

for fname in sorted(p.rglob('*.html')):
    text = fname.read_text(encoding='utf-8')
    open_block = text.count('{%')
    close_block = text.count('%}')
    open_var = text.count('{{')
    close_var = text.count('}}')

    issues = []
    if open_block != close_block:
        issues.append(f"{{% ... %}} mismatch: opens={open_block} closes={close_block}")
    if open_var != close_var:
        issues.append(f"{{{{ ... }}}} mismatch: opens={open_var} closes={close_var}")

    # also check some common misspellings
    typos = []
    for bad in ('endblok', 'end blok', 'end block', 'endbock', 'endblck'):
        if bad in text:
            typos.append(bad)
    if typos:
        issues.append("possible typo(s): " + ", ".join(typos))

    if issues:
        print(f"{fname}:")
        for it in issues:
            print("  -", it)
