import os
from app import create_app

app = create_app()

print("CWD =", os.getcwd())
print("template_folder =", app.template_folder)

index_path = os.path.join(os.getcwd(), app.template_folder, "index.html")
base_path = os.path.join(os.getcwd(), app.template_folder, "base.html")

print("index exists =", os.path.exists(index_path), "->", index_path)
print("base exists  =", os.path.exists(base_path), "->", base_path)
