# Find all REST endpoint patterns in Java
rg -t java -A 3 -B 1 '@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)\(' 

# Find Spring RestTemplate usage
rg -t java -A 5 'RestTemplate|WebClient' --multiline

# Find Python HTTP calls
rg -t py -A 3 'requests\.(get|post|put|delete)|urlopen|httpx\.|aiohttp'

# Find URL constructions
rg -A 3 -B 1 '(String|str).*[Uu]rl.*=' 

# Find configuration loading
rg -g '*.{properties,yml,yaml,json,env}' 'api|endpoint|url|service'

# Trace specific property usage (example for "api.base.url")
rg -t java '@Value\("\$\{api\.base\.url\}"\)|getProperty\("api\.base\.url"\)'