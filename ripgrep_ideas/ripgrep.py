
import subprocess
import json
import re
from pathlib import Path
from typing import List, Dict, Set

class EndpointMigrationTracker:
    def __init__(self, project_root: str, urls: List[str]):
        self.project_root = project_root
        self.urls = urls
        self.findings = {}
        
    def search_literal_urls(self, url: str) -> Dict:
        """Phase 1: Find literal URL occurrences"""
        commands = [
            # Search in all files for exact URL
            ['rg', '--json', '-i', url, self.project_root],
            
            # Search for URL parts (domain, path separately)
            ['rg', '--json', '-i', url.split('/')[-1], self.project_root],
            
            # Search in properties/config files specifically
            ['rg', '--json', '-g', '*.{properties,yml,yaml,json,conf,ini,env}', 
             url, self.project_root],
        ]
        return self._execute_searches(commands)
    
    def search_property_references(self, property_key: str) -> Dict:
        """Phase 2: Find references to property keys"""
        # Common patterns for property access
        patterns = [
            # Java patterns
            f'@Value.*{property_key}',
            f'getProperty.*{property_key}',
            f'getString.*{property_key}',
            f'properties\\.get.*{property_key}',
            
            # Python patterns
            f'config\\[.*{property_key}.*\\]',
            f'os\\.environ.*{property_key}',
            f'settings\\.{property_key}',
            f'get.*{property_key}',
        ]
        
        commands = []
        for pattern in patterns:
            commands.append(['rg', '--json', '-e', pattern, 
                           '-g', '*.{java,py,kt,scala}', self.project_root])
        
        return self._execute_searches(commands)
    
    def search_http_calls(self) -> Dict:
        """Phase 3: Find HTTP client usage patterns"""
        
        # HTTP client patterns for different libraries
        java_patterns = [
            # RestTemplate (Spring)
            'restTemplate\\.(get|post|put|delete|exchange)ForObject',
            'restTemplate\\.exchange',
            
            # WebClient (Spring WebFlux)
            'webClient\\..*\\.(get|post|put|delete)\\(\\)',
            
            # Apache HttpClient
            'HttpGet|HttpPost|HttpPut|HttpDelete',
            'httpClient\\.execute',
            
            # OkHttp
            'Request\\.Builder\\(\\)',
            'okHttpClient\\.newCall',
            
            # Retrofit
            '@(GET|POST|PUT|DELETE)\\(',
            
            # JAX-RS
            '@Path\\(',
        ]
        
        python_patterns = [
            # requests library
            'requests\\.(get|post|put|delete|patch)',
            
            # urllib
            'urllib\\.request\\.urlopen',
            'urllib2\\.urlopen',
            
            # httpx
            'httpx\\.(get|post|put|delete)',
            
            # aiohttp
            'session\\.(get|post|put|delete)',
            'aiohttp\\.ClientSession',
            
            # FastAPI/Flask client calls
            'client\\.(get|post|put|delete)',
        ]
        
        commands = []
        
        # Search Java files
        for pattern in java_patterns:
            commands.append(['rg', '--json', '-e', pattern, 
                           '-g', '*.{java,kt,scala}', '-A', '5', '-B', '2', 
                           self.project_root])
        
        # Search Python files
        for pattern in python_patterns:
            commands.append(['rg', '--json', '-e', pattern, 
                           '-g', '*.py', '-A', '5', '-B', '2', 
                           self.project_root])
        
        return self._execute_searches(commands)
    
    def trace_variable_usage(self, variable_name: str) -> Dict:
        """Phase 4: Trace variable/method usage through the code"""
        
        # Clean variable name (remove special chars that might interfere with regex)
        clean_var = re.escape(variable_name)
        
        commands = [
            # Find variable declarations/assignments
            ['rg', '--json', f'{clean_var}\\s*=', '-g', '*.{java,py,kt,scala}', 
             '-B', '2', '-A', '3', self.project_root],
            
            # Find method calls using the variable
            ['rg', '--json', f'{clean_var}\\.', '-g', '*.{java,py,kt,scala}', 
             '-B', '2', '-A', '3', self.project_root],
            
            # Find where variable is passed as parameter
            ['rg', '--json', f'\\({clean_var}[,\\)]', '-g', '*.{java,py,kt,scala}', 
             '-B', '2', '-A', '3', self.project_root],
        ]
        
        return self._execute_searches(commands)
    
    def _execute_searches(self, commands: List[List[str]]) -> Dict:
        """Execute ripgrep commands and collect results"""
        results = {}
        
        for cmd in commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.stdout:
                    # Parse ripgrep JSON output
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            try:
                                match = json.loads(line)
                                if match.get('type') == 'match':
                                    file_path = match['data']['path']['text']
                                    line_num = match['data']['line_number']
                                    content = match['data']['lines']['text']
                                    
                                    if file_path not in results:
                                        results[file_path] = []
                                    
                                    results[file_path].append({
                                        'line': line_num,
                                        'content': content,
                                        'pattern': ' '.join(cmd[2:])  # Store the search pattern
                                    })
                            except json.JSONDecodeError:
                                continue
            except subprocess.CalledProcessError:
                continue
        
        return results

    def generate_migration_report(self, url: str) -> str:
        """Generate a comprehensive report for migrating a specific endpoint"""
        report = f"\n{'='*60}\nMigration Report for: {url}\n{'='*60}\n\n"
        
        # Phase 1: Direct URL search
        direct_refs = self.search_literal_urls(url)
        report += "1. DIRECT URL REFERENCES:\n"
        for file, matches in direct_refs.items():
            report += f"  📁 {file}\n"
            for match in matches:
                report += f"    Line {match['line']}: {match['content'].strip()}\n"
        
        # Extract property keys if found in config files
        property_keys = self._extract_property_keys(direct_refs)
        
        if property_keys:
            report += f"\n2. PROPERTY KEYS FOUND: {property_keys}\n\n"
            
            # Phase 2: Search for property usage
            for prop_key in property_keys:
                prop_refs = self.search_property_references(prop_key)
                report += f"  Property '{prop_key}' used in:\n"
                for file, matches in prop_refs.items():
                    report += f"    📁 {file}\n"
                    for match in matches:
                        report += f"      Line {match['line']}: {match['content'].strip()}\n"
        
        # Phase 3: Find HTTP calls
        http_calls = self.search_http_calls()
        report += "\n3. HTTP CLIENT USAGE PATTERNS:\n"
        for file, matches in http_calls.items():
            report += f"  📁 {file}\n"
            for match in matches[:3]:  # Limit to first 3 matches per file
                report += f"    Line {match['line']}: {match['content'].strip()}\n"
        
        return report
    
    def _extract_property_keys(self, search_results: Dict) -> Set[str]:
        """Extract property keys from configuration files"""
        property_keys = set()
        
        for file_path, matches in search_results.items():
            if any(ext in file_path for ext in ['.properties', '.yml', '.yaml', '.env']):
                for match in matches:
                    # Extract property key from line like: api.url=https://...
                    content = match['content']
                    if '=' in content:
                        key = content.split('=')[0].strip()
                        property_keys.add(key)
                    elif ':' in content:  # YAML format
                        key = content.split(':')[0].strip()
                        property_keys.add(key)
        
        return property_keys