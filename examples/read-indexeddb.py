#!/usr/bin/env python3
"""
Read Claude Desktop's IndexedDB for cached API data
"""

import sys
from pathlib import Path

try:
    import plyvel
except ImportError:
    print("ERROR: plyvel not installed")
    sys.exit(1)


def read_indexeddb():
    """Read IndexedDB LevelDB"""
    
    indexeddb_path = Path.home() / ".config" / "Claude" / "IndexedDB" / "https_claude.ai_0.indexeddb.leveldb"
    
    if not indexeddb_path.exists():
        print(f"ERROR: IndexedDB not found at {indexeddb_path}")
        return None
    
    try:
        db = plyvel.DB(str(indexeddb_path), create_if_missing=False)
    except Exception as e:
        print(f"ERROR: Cannot open IndexedDB: {e}")
        print("Make sure Claude Desktop is closed")
        return None
    
    print("IndexedDB Keys and Values:")
    print("=" * 60)
    
    for key, value in db:
        key_str = key.decode('utf-8', errors='ignore')
        value_str = value.decode('utf-8', errors='ignore')
        
        print(f"\nKey: {key_str[:100]}")
        print(f"Value length: {len(value)} bytes")
        
        # Try to show readable parts
        if len(value_str) < 1000:
            print(f"Value: {value_str[:500]}")
        else:
            print(f"Value (first 500 chars): {value_str[:500]}")
    
    db.close()


if __name__ == '__main__':
    read_indexeddb()
