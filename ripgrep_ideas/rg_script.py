#!/usr/bin/env python3
import subprocess
import sys
from typing import List, Dict

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
    # Service endpoints to migrate: {service_name: endpoint_path}
    service_endpoints: Dict[str, str] = {
        "cca": "/v1/cca",
        "chats": "/v1/chat/?cname",
        # Add more service endpoints here
    }

    for service_name, endpoint in service_endpoints.items():
        print(f"\n{'='*60}")
        print(f"Service: {service_name}")
        print(f"Endpoint: {endpoint}")
        print('='*60)

        # Search for direct endpoint path references
        print("\n1. Direct endpoint references:")
        print(run_ripgrep_search(endpoint))

        # Search for service name references
        print(f"\n2. Service name references ({service_name}):")
        print(run_ripgrep_search(service_name))

        # Search for common HTTP patterns
        print("\n3. HTTP client usage:")
        print(run_ripgrep_search('(RestTemplate|requests|HttpClient|WebClient)',
                                ['java', 'py']))

if __name__ == "__main__":
    main()