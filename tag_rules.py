import re

def auto_tag(path):
    name = path.name.lower()
    tags = set()

    if "tax" in name:
        tags.add("taxes")

    if match := re.search(r"\b(20\d{2})\b", name):
        tags.add(match.group(1))

    ext = path.suffix.lower()
    if ext in [".txt", ".md", ".rst"]:
        tags.add("text")
    elif ext in [".jpg", ".jpeg", ".png", ".gif"]:
        tags.add("image")
    elif ext == ".pdf":
        tags.add("document")
    elif ext in [".mp3", ".wav", ".flac"]:
        tags.add("audio")
    elif ext in [".mp4", ".mkv", ".avi"]:
        tags.add("video")

    return sorted(tags)
