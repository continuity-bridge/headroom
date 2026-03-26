#!/usr/bin/env python3
"""
claude-api-sniffer - Capture Claude Desktop's API calls

Uses tcpdump/tshark to capture HTTP(S) traffic to anthropic.com
and extract the usage API endpoint.

Requirements:
    sudo apt install tshark
    # OR
    sudo pacman -S wireshark-cli

Author: Uncle Tallest & Vector
Created: 2026-03-25
"""

import subprocess
import sys
from pathlib import Path


def check_tshark():
    """Check if tshark is installed"""
    try:
        subprocess.run(['tshark', '--version'], 
                      capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def sniff_traffic():
    """Capture HTTP traffic to anthropic.com"""
    
    print("Starting network capture...")
    print("=" * 60)
    print()
    print("Instructions:")
    print("1. This script will start capturing network traffic")
    print("2. Open Claude Desktop")
    print("3. Go to Settings → Usage")
    print("4. Wait a few seconds")
    print("5. Press Ctrl+C to stop capture")
    print()
    print("Looking for requests to anthropic.com...")
    print("=" * 60)
    print()
    
    # Capture HTTPS traffic to anthropic.com
    cmd = [
        'sudo', 'tshark',
        '-i', 'any',  # All interfaces
        '-f', 'host api.anthropic.com or host claude.ai',  # Filter
        '-Y', 'http or http2 or tls',  # Display filter
        '-T', 'fields',
        '-e', 'frame.number',
        '-e', 'http.request.method',
        '-e', 'http.request.uri',
        '-e', 'http.host',
        '-e', 'http2.headers.path',
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print()
        print("Capture stopped")
        print()
        print("If you saw any API requests above, note the URL/path")
        print("We can use that to query usage data directly!")
    

def main():
    if not check_tshark():
        print("ERROR: tshark not installed", file=sys.stderr)
        print()
        print("Install with:")
        print("  sudo apt install tshark")
        print("  # OR")
        print("  sudo pacman -S wireshark-cli")
        return 1
    
    print("Note: This requires root/sudo to capture network traffic")
    print()
    
    sniff_traffic()
    return 0


if __name__ == '__main__':
    sys.exit(main())
