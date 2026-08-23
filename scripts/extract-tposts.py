from pathlib import Path
import re
html = Path(r"C:\Users\Илья\cenzyk-art\tmp-live-home.html").read_text(encoding="utf-8", errors="ignore")
links = sorted(set(re.findall(r"https://cenzyk\.art/tpost/[a-zA-Z0-9_-]+", html)))
print("links", links)
# also relative
rel = sorted(set(re.findall(r"/tpost/[a-zA-Z0-9_-]+", html)))
print("rel", rel)
