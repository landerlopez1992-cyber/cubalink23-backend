#!/usr/bin/env python3
import re
with open("admin_routes.py", "r") as f:
    content = f.read()
content = content.replace("air/suggestions?query={query}&limit=20", "air/airports?search={query}&limit=20")
with open("admin_routes.py", "w") as f:
    f.write(content)
print("✅ URL corregida")
