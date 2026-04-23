from pathlib import Path
from src import csv_handler, downloader, image_processor, api_client

def run_pipeline():
    csv_file = Path("data/form_responses.csv")
    
    # 1. Parse CSV
    print("Reading CSV...")
    entries = csv_handler.parse_csv(csv_file)
    
    for entry in entries:
        name = entry['name']
        print(f"--- Processing {name} ---")
        student_dir = Path("profiles") / name
        
        # 2. Download
        downloader.download_profile_images(entry['meta'], student_dir)
        
        # # 3. Convert
        # image_processor.process_all_in_folder(student_dir)
        
        # 4. API Update
        api_client.update_cover_via_api(student_dir, entry['meta'])
        
        print(f"✅ Finished {name}")

if __name__ == "__main__":
    run_pipeline()
    print("\nAll done! Everyone is processed.")