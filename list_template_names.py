import os
p = os.path.join("templates", "student")
print("Listing directory:", os.path.abspath(p))
for f in os.listdir(p):
    full = os.path.join(p, f)
    print(repr(f), "-", os.path.getsize(full), "bytes  ->", full)
