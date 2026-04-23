import requests
import re
import os
from pathlib import Path
from PIL import Image
import pillow_heif  # Needed for HEIC support

# Register HEIF opener once
pillow_heif.register_heif_opener()

def get_direct_url(url: str):
    if not url: return None
    match = re.search(r'(?:/d/|id=)([a-zA-Z0-9_-]+)', url)
    return f"https://drive.google.com/uc?export=download&id={match.group(1)}" if match else None

def download_file(url: str, output_dir: Path, base_name: str):
    if not url: return
    try:
        direct_url = get_direct_url(url)
        if not direct_url: return
        
        response = requests.get(direct_url, stream=True, timeout=10)
        response.raise_for_status()
        
        # 1. Download to a temporary file first
        temp_path = output_dir / f"{base_name}.temp"
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(8192):
                f.write(chunk)
        
        # 2. Attempt to open as an image to detect its real format
        try:
            with Image.open(temp_path) as img:
                # Get the format (e.g., 'JPEG', 'HEIF', 'PNG')
                img_format = img.format
                
                # Create the final path for the JPG
                jpg_path = output_dir / f"{base_name}.jpg"
                
                # Convert and save as JPG
                img.convert("RGB").save(jpg_path, "JPEG", quality=95)
                
                print(f"    ✅ Successfully processed {base_name} ({img_format} -> JPG)")
                
                # Remove the temp file
                os.remove(temp_path)
                
        except Exception:
            # If it fails to open as an image, it might not be an image. 
            # Rename temp to .bin or keep as is.
            print(f"    ⚠️ File {base_name} is not a recognizable image. Saving as binary.")
            os.rename(temp_path, output_dir / f"{base_name}.bin")
                
    except Exception as e:
        print(f"    ⚠️ Download failed for {base_name}: {e}")

def download_profile_images(meta, student_dir):
    if meta.get('cover_url'):
        download_file(meta['cover_url'], student_dir, "raw_cover")
    
    add_urls = meta.get('additional_urls', [])
    if add_urls:
        add_dir = student_dir / "additional"
        add_dir.mkdir(exist_ok=True)
        for i, url in enumerate(add_urls):
            download_file(url, add_dir, f"extra_{i}")