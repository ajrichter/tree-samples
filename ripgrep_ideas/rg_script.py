#!/usr/bin/env python3
import subprocess
import sys
from typing import List

def run_ripgrep_search(pattern: str, file_types: List[str] = None, 
                       context_before: int = 2, context_after: int = 3) -> str:
    """Execute a ripgrep search with given parameters"""
    
    cmd = ['rg', '--no-heading', '--line-number', '--color=never']
    
    # Add context lines
    if context_before > 0:
        cmd.extend(['-B', str(context_before)])
    if context_after > 0:
        cmd.extend(['-A', str(context_after)])
    
    # Add file type filters
    if file_types:
        for ft in file_types:
            cmd.extend(['-t', ft])
    
    # Add the search pattern
    cmd.append(pattern)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return result.stdout
    except FileNotFoundError:
        print("Error: ripgrep (rg) is not installed")
        sys.exit(1)

def main():
    # Your list of URLs to migrate
    urls_to_migrate = [
        "https://api.example.com/v1/users",
        "https://legacy-service.internal/data",
        # Add more URLs here
    ]
    
    for url in urls_to_migrate:
        print(f"\n{'='*60}")
        print(f"Searching for: {url}")
        print('='*60)
        
        # Search for direct URL usage
        print("\n1. Direct URL references:")
        print(run_ripgrep_search(url))
        
        # Search for domain only (might be constructed dynamically)
        domain = url.split('/')[2]
        print(f"\n2. Domain references ({domain}):")
        print(run_ripgrep_search(domain))
        
        # Search for common HTTP patterns near this domain
        print("\n3. HTTP client usage:")
        print(run_ripgrep_search('(RestTemplate|requests|HttpClient|WebClient)', 
                                ['java', 'py']))

if __name__ == "__main__":
    main()