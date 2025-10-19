"""
Simple script to read first few lines from galaxy.json.gz without loading everything into memory.
"""

import json
import gzip
import datetime


def read_first_entries_simple(file_path: str, n: int = 10):
    """
    Simple approach: reads the file line by line assuming each line is a JSON object.
    If that doesn't work, tries to parse as array.
    """
    entries = []
    
    try:
        with gzip.open(file_path, "rt", encoding="utf-8") as f:
            # Try line-by-line first (if it's JSONL format)
            for i, line in enumerate(f):
                if i >= n:
                    break
                line = line.strip()
                if line and not line.startswith('[') and not line.endswith(']'):
                    try:
                        entry = json.loads(line.rstrip(','))
                        entries.append(entry)
                    except json.JSONDecodeError:
                        continue
            
            # If we didn't get any entries, try parsing as array
            if not entries:
                f.seek(0)
                content = f.read(100000)  # Read first 100KB
                
                # Find first complete objects
                start_idx = content.find('{')
                if start_idx != -1:
                    # Find up to n complete objects
                    bracket_count = 0
                    current_start = start_idx
                    
                    for i, char in enumerate(content[start_idx:], start_idx):
                        if char == '{':
                            bracket_count += 1
                        elif char == '}':
                            bracket_count -= 1
                            
                        if bracket_count == 0 and len(entries) < n:
                            obj_str = content[current_start:i+1]
                            try:
                                entry = json.loads(obj_str)
                                entries.append(entry)
                                # Find next object start
                                next_start = content.find('{', i+1)
                                if next_start == -1:
                                    break
                                current_start = next_start
                            except json.JSONDecodeError:
                                pass
                            
    except Exception as e:
        print(f"Error reading file: {e}")
    
    return entries


def main():
    start_time = datetime.datetime.now()
    
    galaxy_file_path = "galaxy.json.gz"
    
    print(f"Reading first 10 entries from {galaxy_file_path}...")
    entries = read_first_entries_simple(galaxy_file_path, 10)
    
    print(f"\nFound {len(entries)} entries:")
    print("=" * 60)
    
    for i, entry in enumerate(entries, 1):
        print(f"\nEntry {i}:")
        print(json.dumps(entry, indent=2))
        print("-" * 40)
    
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"\nProcessing time: {duration}")


if __name__ == "__main__":
    main()