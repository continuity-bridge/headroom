#!/usr/bin/env python3
"""
claude-usage-simple-reader - Extract usage from Claude Desktop without plyvel

Brute-force reads Claude's LevelDB files as binary and extracts JSON data.
No external dependencies needed!

Author: Uncle Tallest & Vector  
Created: 2026-03-25
"""

import re
import json
from pathlib import Path


def extract_json_from_binary(data: bytes):
    """Extract JSON objects from binary data"""
    # Look for JSON-like patterns in the binary data
    text = data.decode('utf-8', errors='ignore')
    
    # Find all JSON objects
    json_objects = []
    
    # Pattern 1: Look for {...} blocks
    brace_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.finditer(brace_pattern, text, re.DOTALL)
    
    for match in matches:
        try:
            obj = json.loads(match.group())
            json_objects.append(obj)
        except:
            pass
    
    return json_objects


def read_leveldb_files(leveldb_dir: Path):
    """Read all .ldb files and extract JSON"""
    all_data = {}
    
    for ldb_file in leveldb_dir.glob('*.ldb'):
        print(f"Reading {ldb_file.name}...")
        
        try:
            with open(ldb_file, 'rb') as f:
                data = f.read()
            
            json_objects = extract_json_from_binary(data)
            
            if json_objects:
                all_data[ldb_file.name] = json_objects
                print(f"  Found {len(json_objects)} JSON objects")
        
        except Exception as e:
            print(f"  Error reading {ldb_file.name}: {e}")
    
    return all_data


def main():
    print("Claude Desktop Usage Reader (Simple)")
    print("=" * 50)
    print()
    
    config_dir = Path.home() / ".config" / "Claude"
    leveldb_dir = config_dir / "Local Storage" / "leveldb"
    
    if not leveldb_dir.exists():
        print(f"ERROR: LevelDB directory not found: {leveldb_dir}")
        return 1
    
    print("Extracting JSON from LevelDB files...")
    print()
    
    data = read_leveldb_files(leveldb_dir)
    
    if not data:
        print("No JSON data found")
        return 1
    
    # Look for usage-related data
    print()
    print("Searching for usage-related data...")
    print()
    
    for filename, objects in data.items():
        for obj in objects:
            obj_str = json.dumps(obj, indent=2)
            
            # Check if this object contains usage-related keys
            if any(term in obj_str.lower() for term in ['usage', 'limit', 'quota', 'rate', 'remaining']):
                print(f"Found in {filename}:")
                print(obj_str)
                print()
    
    # Save everything to a file for inspection
    output_file = Path("claude-leveldb-dump.json")
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Full dump saved to: {output_file}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
