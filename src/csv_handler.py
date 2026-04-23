import csv
import json
from pathlib import Path

def parse_csv(csv_path: Path):
    entries = []
    if not csv_path.exists():
        print(f"❌ File not found: {csv_path}")
        return []

    with open(csv_path, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Profile Created?') == 'Yes':
                continue
            
            name = row.get('Full Name', 'Unknown').strip()
            if not name: continue # Skip if name is completely missing

            student_dir = Path("profiles") / name
            student_dir.mkdir(exist_ok=True)
            
            # Use .get() to avoid KeyErrors
            meta = {
                "name": name,
                "major": row.get('Admitted Major', ''),
                "location": row.get('Country / City', ''),
                "handle": row.get('Instagram Handle (optional)', ''),
                "cover_url": row.get('Cover Image (Preferably in the aspect ratio 1:1) (may need to be compressed to <10MB)', '').strip(),
                "additional_urls": [u.strip() for u in row.get('Additional Images (optional) (may need to be compressed to <10MB)', '').split(',') if u.strip()],
                "caption": row.get('Caption for Post (optional)', '').strip(),
                "song": row.get('Song for Post (include artist name for ease) (optional)', '').strip(),
                "profile_created": row.get('Profile Created?', 'No').strip() == 'Yes',
                "posted": row.get('Posted?', 'No').strip() == 'Yes'
            }
            
            with open(student_dir / "profile.json", "w") as jf:
                json.dump(meta, jf, indent=4)
                
            entries.append({"name": name, "meta": meta})
    return entries