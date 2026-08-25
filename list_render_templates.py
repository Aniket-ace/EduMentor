# list_render_templates.py
import re, pathlib
p = pathlib.Path('.')
pattern = re.compile(r'render_template\(\s*[\'"]([^\'"]+\.html)[\'"]')
found = set()
for fname in p.rglob('*.py'):
    text = fname.read_text(errors='ignore')
    for m in pattern.findall(text):
        found.add(m)
if not found:
    print("No render_template('*.html') calls found")
else:
    print("Templates referenced by render_template in code:")
    for t in sorted(found):
        print(" -", t)
