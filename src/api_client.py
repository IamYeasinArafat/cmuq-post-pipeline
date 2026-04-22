import requests
from pathlib import Path

def update_cover_via_api(student_dir: Path, meta):
    cover_path = student_dir / "cover.jpg"
    
    # Don't call API if the cover image wasn't successfully created
    if not cover_path.exists():
        print("    ℹ️ Skipping API call: No cover.jpg found.")
        return

    url = "http://127.0.0.1:8000/v3/generate-profile"
    params = {
        "name": meta.get('name', 'N/A'),
        "major": meta.get('major', 'N/A'),
        "location": meta.get('location', 'N/A'),
        "handle": meta.get('handle', 'N/A')
    }
    
    try:
        with open(cover_path, "rb") as f:
            files = {"profile_file": ("cover.jpg", f, "image/jpeg")}
            response = requests.post(url, params=params, files=files)
            response.raise_for_status()
            
            with open(cover_path, "wb") as f:
                f.write(response.content)
            print("    ✅ API Updated cover successfully.")
    except Exception as e:
        print(f"    ❌ API Request failed: {e}")