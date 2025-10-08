# Migrating Legacy Python REST Codebase to GraphQL

## Strategies to Identify Legacy REST Code

### Framework-specific patterns

**Search for REST framework imports and decorators:**
- Flask: `@app.route`, `@blueprint.route`, `from flask import`
- Django REST Framework: `@api_view`, `APIView`, `ViewSet`, `serializers.Serializer`
- FastAPI: `@app.get`, `@app.post`, `APIRouter`
- Tornado: `RequestHandler`, `Application`

### Code structure analysis

**Find API endpoints:**
- URL/route definitions (urls.py, route decorators)
- HTTP method handlers (GET, POST, PUT, DELETE, PATCH)
- Request/response serializers and validators
- API versioning patterns (e.g., `/api/v1/`)

**Identify business logic tied to REST:**
- View classes and functions
- Serializer/deserializer code
- Pagination, filtering, sorting implementations
- Authentication/authorization decorators

### Automated discovery

**Use grep/ripgrep to find:**
- `@route`, `@api_view`, `@action` decorators
- `request.method`, `request.GET`, `request.POST`
- `Response(`, `JsonResponse(`, `render(`
- `status_code`, HTTP status constants

**Analyze dependencies:**
- Check requirements.txt for REST frameworks
- Map which modules import REST-specific libraries

### Documentation & traffic analysis

- Parse OpenAPI/Swagger specs if they exist
- Review API documentation
- Analyze access logs to identify active endpoints
- Check frontend code for API calls

---

## Mapping Python to Java: Tracing from Endpoints to All Related Files

### Step 1: Start with the endpoint definition

**Locate the endpoint handler:**
- Search for the route/URL pattern in your Python codebase
- Identify the view function or class that handles the endpoint
- Note the file path and function/class name

### Step 2: Trace dependencies backward from endpoints

**Build a dependency graph:**
- Use static analysis tools (e.g., `pydeps`, `import-deps`, `pipreqs`)
- Parse import statements to map module relationships
- Create a tree showing what each endpoint file imports

**Manual dependency tracing:**
- Start from the endpoint handler function
- Follow all function calls within the handler
- Track all imported modules and classes
- Identify all database models/ORM entities used
- Find all serializers, validators, and data transformers
- Locate utility functions and helper modules

### Step 3: Categorize files by function

**Group files into layers:**
- **Controller/View layer**: Endpoint handlers and routing
- **Service/Business logic layer**: Core business rules and operations
- **Data access layer**: Database queries, ORM models, repositories
- **Serialization layer**: Request/response transformers, validators
- **Utility layer**: Helpers, constants, configurations
- **Middleware/Interceptors**: Authentication, logging, error handling
- **External integrations**: Third-party API clients, message queues

### Step 4: Automated analysis techniques

**Static code analysis:**
```bash
# Find all imports in a file
grep -r "^import\|^from" endpoint_file.py

# Find all function calls (simplified)
grep -oE "[a-z_][a-z0-9_]*\(" endpoint_file.py

# Use AST parsing to build call graphs
python -m ast endpoint_file.py
```

**Dynamic analysis:**
- Enable Python profiling/tracing (`sys.settrace`, `trace` module)
- Run tests with coverage to identify executed code paths
- Use debugger to step through endpoint execution
- Log all module imports at runtime

**Dependency visualization tools:**
- `pycallgraph`: Generate call graphs
- `snakeviz`: Visualize profiling data
- `pydeps`: Create module dependency graphs
- Custom scripts using `ast` module to parse imports

### Step 5: Cross-reference with database schema

**Map data flow:**
- Identify all database tables accessed by each endpoint
- Trace ORM model usage (e.g., Django models, SQLAlchemy)
- Find all raw SQL queries
- Document database relationships (foreign keys, joins)
- Map Python models → Java entities

### Step 6: Identify shared/common code

**Find code used by multiple endpoints:**
- Authentication/authorization modules
- Common validators and serializers
- Shared business logic
- Database connection pooling
- Configuration management
- Logging and monitoring utilities

### Step 7: Create migration manifest

**For each endpoint, document:**
- Endpoint URL and HTTP method
- Python handler file and function
- All imported modules (with file paths)
- Database models/tables accessed
- External dependencies (Redis, queues, APIs)
- Middleware applied to this endpoint
- Tests associated with this endpoint
- Equivalent Java package structure

**Example manifest entry:**
```
Endpoint: GET /api/v1/users/{id}
Python Handler: src/views/user_views.py::get_user()
Dependencies:
  - src/services/user_service.py
  - src/models/user.py
  - src/models/profile.py
  - src/serializers/user_serializer.py
  - src/utils/cache.py
Database: users, profiles
Java Mapping:
  - com.app.controller.UserController::getUser()
  - com.app.service.UserService
  - com.app.model.User, Profile
  - com.app.dto.UserResponse
```

### Step 8: Automated tools for Python → Java mapping

**Static analysis scripts:**
- Write Python scripts using `ast` module to parse all files
- Extract imports, function definitions, class definitions
- Build a JSON/YAML manifest of all dependencies
- Generate dependency matrices (endpoint → files)

**Suggested toolchain:**
- `jedi` or `rope`: Python code analysis libraries
- `graphviz`: Visualize dependency graphs
- Custom scripts to output CSV/JSON for tracking
- Code search tools (ripgrep, ag) with regex patterns

**Example Python script approach:**
```python
import ast
import os

def analyze_endpoint_dependencies(endpoint_file):
    with open(endpoint_file) as f:
        tree = ast.parse(f.read())

    imports = [node for node in ast.walk(tree)
               if isinstance(node, (ast.Import, ast.ImportFrom))]
    functions = [node for node in ast.walk(tree)
                 if isinstance(node, ast.FunctionDef)]

    # Extract and map dependencies
    return {
        'imports': imports,
        'functions': functions,
        # ... more analysis
    }
```
