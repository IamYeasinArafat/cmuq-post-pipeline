from pathlib import Path
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

def process_all_in_folder(student_dir: Path):
    # Process Cover - only if raw_cover exists
    raw_cover = student_dir / "raw_cover.png"
    if raw_cover.exists():
        try:
            with Image.open(raw_cover) as img:
                img.convert("RGB").save(student_dir / "cover.jpg", "JPEG", quality=95)
        except Exception as e:
            print(f"    ⚠️ Cover processing failed: {e}")
    else:
        print("    ℹ️ No cover image to process.")
    
    # Process Additional
    add_dir = student_dir / "additional"
    if add_dir.exists():
        for img_path in add_dir.iterdir():
            try:
                with Image.open(img_path) as img:
                    img.convert("RGB").save(img_path.with_suffix(".jpg"), "JPEG", quality=95)
            except Exception as e:
                print(f"    ⚠️ Skipping {img_path.name}: {e}")