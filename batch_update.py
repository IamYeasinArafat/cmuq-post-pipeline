from pathlib import Path
import json
from src.api_client import update_cover_via_api

def batch_update():
    profiles_dir = Path("profiles")
    
    for student_folder in profiles_dir.iterdir():
        if student_folder.is_dir():
            json_file = student_folder / "profile.json"
            cover_file = student_folder / "cover.jpg"
            
            if json_file.exists() and cover_file.exists():
                print(f"🔄 Updating API for: {student_folder.name}")
                with open(json_file, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                
                # Re-using the function we wrote earlier
                update_cover_via_api(student_folder, meta, bg_version="v1")
            else:
                print(f"⚠️ Skipping {student_folder.name}: Missing profile.json or cover.jpg")

if __name__ == "__main__":
    batch_update()