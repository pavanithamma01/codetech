import hashlib
import os
import json

# Path to monitor
FOLDER_TO_MONITOR = "sample_folder"  # Change this to your target folder
HASH_RECORD_FILE = "hash_record.json"

# Function to calculate SHA-256 hash
def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

# Create or load the hash record
def load_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, "r") as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_RECORD_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

def scan_files():
    new_hashes = {}
    for root, _, files in os.walk(FOLDER_TO_MONITOR):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_hash = calculate_hash(file_path)
            new_hashes[file_path] = file_hash
    return new_hashes

def compare_hashes(old, new):
    modified = []
    for path, new_hash in new.items():
        old_hash = old.get(path)
        if old_hash and old_hash != new_hash:
            modified.append(path)
    return modified

def main():
    print("Scanning files...")
    previous_hashes = load_hashes()
    current_hashes = scan_files()
    changes = compare_hashes(previous_hashes, current_hashes)

    if changes:
        print("Modified files:")
        for file in changes:
            print(f"- {file}")
    else:
        print("No changes detected.")

    save_hashes(current_hashes)

if __name__ == "__main__":
    main()