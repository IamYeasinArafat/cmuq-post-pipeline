import requests
import re
from pathlib import Path

def get_direct_url(url: str):
    if not url: return None
    match = re.search(r'(?:/d/|id=)([a-zA-Z0-9_-]+)', url)
    return f"https://drive.google.com/uc?export=download&id={match.group(1)}" if match else None

def download_file(url: str, save_path: Path):
    if not url: return
    try:
        direct_url = get_direct_url(url)
        if not direct_url: return
        response = requests.get(direct_url, stream=True, timeout=10)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
    except Exception as e:
        print(f"    ⚠️ Download failed for {save_path.name}: {e}")

def download_profile_images(meta, student_dir):
    # Only download if URL exists
    if meta.get('cover_url'):
        download_file(meta['cover_url'], student_dir / "raw_cover.png")
    
    add_urls = meta.get('additional_urls', [])
    if add_urls:
        add_dir = student_dir / "additional"
        add_dir.mkdir(exist_ok=True)
        for i, url in enumerate(add_urls):
            download_file(url, add_dir / f"extra_{i}.png")