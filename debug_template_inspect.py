# debug_template_inspect.py
import pathlib, re, sys

root = pathlib.Path('.')

print("== Searching for includes, render_template_string, and render_template(...) calls in Python files ==")
py_pattern_inc = re.compile(r'{%\s*include\s+[\'"]([^\'"]+)[\'"]\s*%}')
py_pattern_render_str = re.compile(r'render_template_string\(')
py_pattern_render = re.compile(r'render_template\(\s*[\'"]([^\'"]+\.html)[\'"]')

referenced_templates = set()
includes_found = []

for p in root.rglob('*.py'):
    text = p.read_text(errors='ignore')
    for m in py_pattern_render.findall(text):
        referenced_templates.add(m)
    if py_pattern_render_str.search(text):
        print(f" - render_template_string(...) found in {p}")
    # Also search for jinja include usage INSIDE python strings (rare)
    for m in re.findall(r'{%\s*include\s+[\'"]([^\'"]+)[\'"]', text):
        includes_found.append((p, m))

if referenced_templates:
    print("Templates referenced by render_template(...) in python code:")
    for t in sorted(referenced_templates):
        print("  -", t)
else:
    print("No explicit render_template('*.html') calls found in python files (or none detected).")

if includes_found:
    print("\nPossible include template names found inside python files:")
    for p,inc in includes_found:
        print(f"  {p}: include -> {inc}")
else:
    print("No include-like strings found inside python files.")

print("\n== Now scanning templates/ - printing last 40 lines of each .html template (to spot abrupt endings) ==")
tpath = pathlib.Path('templates')
if not tpath.exists():
    print("No templates directory found.")
    sys.exit(0)

for f in sorted(tpath.rglob('*.html')):
    text = f.read_text(encoding='utf-8', errors='replace')
    lines = text.splitlines()
    tail = "\n".join(lines[-40:]) if len(lines) > 40 else "\n".join(lines)
    print("\n" + "="*80)
    print(f"FILE: {f} (last {min(40, len(lines))} lines)")
    print("="*80)
    print(tail)
    # quick heuristic checks
    if text.rstrip().endswith('{%') or text.rstrip().endswith('{{'):
        print("\n>>> WARNING: file ends with an open Jinja tag (endswith '{%' or '{{')\n")
    # check for stray endblok-like typos
    for typo in ('endblok', 'end blok', 'end block', 'endbock', 'endbock'):
        if typo in text:
            print(f"\n>>> WARNING: possible typo '{typo}' found in {f}\n")
