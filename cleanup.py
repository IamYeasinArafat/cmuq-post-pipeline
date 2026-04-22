from pathlib import Path

def cleanup_additional_folders():
    profiles_dir = Path("profiles")
    
    for student_folder in profiles_dir.iterdir():
        additional_dir = student_folder / "additional"
        
        if additional_dir.exists() and additional_dir.is_dir():
            print(f"📂 Checking folder: {student_folder.name}")
            
            for file_path in additional_dir.iterdir():
                # Check if the file suffix is NOT .jpg (case insensitive)
                if file_path.suffix.lower() != '.jpg':
                    print(f"  🗑️ Deleting non-jpg file: {file_path.name}")
                    file_path.unlink()  # This deletes the file

if __name__ == "__main__":
    # Optional: Add a confirmation prompt if you want to be extra safe
    confirm = input("This will permanently delete non-JPG files. Continue? (y/n): ")
    if confirm.lower() == 'y':
        cleanup_additional_folders()
        print("✅ Cleanup complete.")
    else:
        print("❌ Cleanup aborted.")