import json, os, shutil, sys
from pathlib import Path

def find_bookmarks(start):
    for p in [os.path.join(start, "Data", "profile", "Default", "Bookmarks"),
              os.path.join(start, "User Data", "Default", "Bookmarks"),
              os.path.join(start, "Default", "Bookmarks")]:
        if os.path.isfile(p): return p
    for root, dirs, files in os.walk(start):
        if "Bookmarks" in files:
            try:
                with open(os.path.join(root, "Bookmarks"), "r", encoding="utf-8") as f:
                    if "roots" in json.load(f): return os.path.join(root, "Bookmarks")
            except: continue
    return None

def dedupe(children, seen, removed):
    result = []
    for item in children:
        if item.get("type") == "url":
            key = (item.get("url", ""), item.get("name", ""))
            if key in seen: removed.append(item)
            else: seen.add(key); result.append(item)
        elif item.get("type") == "folder":
            if "children" in item: item["children"] = dedupe(item["children"], seen, removed)
            result.append(item)
        else: result.append(item)
    return result

def main():
    path = find_bookmarks(os.path.dirname(os.path.abspath(__file__)))
    if not path: print("ERROR: Bookmarks not found."); sys.exit(1)
    print(f"Found: {path}")
    shutil.copy2(path, path + ".backup")
    with open(path, "r", encoding="utf-8") as f: data = json.load(f)
    seen, removed = set(), []
    for k, v in data.get("roots", {}).items():
        if isinstance(v, dict) and "children" in v:
            v["children"] = dedupe(v["children"], seen, removed)
    data.pop("checksum", None)
    print(f"Kept: {len(seen)} | Removed: {len(removed)}")
    if removed:
        with open(path, "w", encoding="utf-8") as f: json.dump(data, f, indent=3)
        print("Done. Close Chrome BEFORE running this.")

if __name__ == "__main__": main()
