from pathlib import Path
from datetime import datetime
import hashlib
import yaml
from tag_rules import auto_tag

def compute_checksum(path, block_size=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(block_size):
            h.update(chunk)
    return h.hexdigest()

def scan_dir(root_dir):
    root_path = Path(root_dir).resolve()
    entries = []

    for file_path in root_path.rglob("*"):
        if not file_path.is_file():
            continue

        rel_path = file_path.relative_to(root_path).as_posix()
        stat = file_path.stat()

        entry = {
            "path": rel_path,
            "size_bytes": stat.st_size,
            "mod_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "checksum": compute_checksum(file_path),
            "tags": auto_tag(file_path)
        }

        entries.append(entry)

    return {
        "generated_at": datetime.now().isoformat(),
        "root": str(root_path),
        "files": entries
    }

def main():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python tagger.py /path/to/directory")
        return

    root_dir = sys.argv[1]
    data = scan_dir(root_dir)

    out_path = Path("semantic_index.yaml")
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False, allow_unicode=True)

    print(f"Generated semantic_index.yaml with {len(data['files'])} entries.")

if __name__ == "__main__":
    main()