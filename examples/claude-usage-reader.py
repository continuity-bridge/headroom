#!/usr/bin/env python3
"""
claude-usage-reader - Extract usage data from Claude Desktop

Reads Claude Desktop's LocalStorage LevelDB to get real usage statistics.

Requirements:
    pip install plyvel --break-system-packages

Author: Uncle Tallest & Vector
Created: 2026-03-25
"""

import sys
import json
from pathlib import Path

try:
    import plyvel
except ImportError:
    print("ERROR: plyvel not installed", file=sys.stderr)
    print("Install with: pip install plyvel --break-system-packages", file=sys.stderr)
    sys.exit(1)


def read_leveldb_database(db_path: Path, db_name: str):
    """Read a LevelDB database and extract usage data"""
    if not db_path.exists():
        return None
    
    try:
        db = plyvel.DB(str(db_path), create_if_missing=False)
    except Exception as e:
        print(f"ERROR: Cannot open {db_name}: {e}", file=sys.stderr)
        if "lock" in str(e).lower():
            print("Make sure Claude Desktop is closed", file=sys.stderr)
        return None
    
    usage_data = {}
    
    # Iterate through all keys
    for key, value in db:
        key_str = key.decode('utf-8', errors='ignore')
        
        # Look for keys that might contain usage info
        if any(term in key_str.lower() for term in ['usage', 'limit', 'quota', 'rate']):
            try:
                value_str = value.decode('utf-8', errors='ignore')
                if value_str.startswith('{') or value_str.startswith('['):
                    usage_data[key_str] = json.loads(value_str)
                else:
                    usage_data[key_str] = value_str
            except:
                usage_data[key_str] = f"<binary data: {len(value)} bytes>"
    
    db.close()
    return usage_data


def read_claude_usage():
    """Read usage data from Claude Desktop's storage"""
    config_dir = Path.home() / ".config" / "Claude"
    
    all_usage = {}
    
    # Try LocalStorage
    localstorage_path = config_dir / "Local Storage" / "leveldb"
    print("Checking LocalStorage...")
    ls_data = read_leveldb_database(localstorage_path, "LocalStorage")
    if ls_data:
        all_usage.update(ls_data)
    
    # Try IndexedDB (note: this might fail with comparator error, that's OK)
    indexeddb_path = config_dir / "IndexedDB" / "https_claude.ai_0.indexeddb.leveldb"
    print("Checking IndexedDB...")
    idb_data = read_leveldb_database(indexeddb_path, "IndexedDB")
    if idb_data:
        all_usage.update(idb_data)
    
    return all_usage if all_usage else None


def main():
    print("Claude Desktop Usage Reader")
    print("=" * 50)
    print()
    print("Reading LocalStorage LevelDB...")
    print()
    
    usage = read_claude_usage()
    
    if not usage:
        print("No usage data found")
        return 1
    
    print(f"Found {len(usage)} usage-related keys:")
    print()
    
    for key, value in usage.items():
        print(f"Key: {key}")
        if isinstance(value, (dict, list)):
            print(f"Value: {json.dumps(value, indent=2)}")
        else:
            print(f"Value: {value}")
        print()
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
