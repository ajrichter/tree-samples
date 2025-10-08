# High-Level Explanation: Java AST Agent System

## Table of Contents
1. [Overview](#overview)
2. [Directory Structure](#directory-structure)
3. [Core Architecture](#core-architecture)
4. [Treesitter Tree Construction](#treesitter-tree-construction)
5. [How Agents Use the Tree to Modify Code](#how-agents-use-the-tree-to-modify-code)
6. [Main Methods and Components](#main-methods-and-components)
7. [Testing Approach](#testing-approach)
8. [Adding New Examples](#adding-new-examples)
9. [Workflow Execution](#workflow-execution)
10. [Common Use Cases](#common-use-cases)

---

## Overview

This project is a **Treesitter-based Java code analysis and refactoring system** that uses **LangGraph agents** to parse, analyze, and modify Java source code. The system provides a powerful framework for automated code refactoring, pattern recognition, and structural modifications.

### Key Technologies
- **Treesitter**: Fast, incremental parsing library for building Abstract Syntax Trees (AST)
- **LangGraph**: Agent-based workflow orchestration framework
- **Python**: Implementation language for agents and workflows
- **tree-sitter-java**: Java language grammar for Treesitter

---

## Directory Structure

```
treesitter-mockup/
├── src/                          # Main source code directory
│   ├── agents/                   # LangGraph agent implementations
│   │   ├── base_agent.py        # Base class for all agents
│   │   ├── parser_agent.py      # Parsing and basic info extraction
│   │   ├── analyzer_agent.py    # Code structure analysis
│   │   ├── editor_agent.py      # Code modification operations
│   │   ├── java_patterns.py     # Java pattern recognition
│   │   ├── java_refactoring.py  # Java-specific refactoring
│   │   ├── advanced_refactoring.py  # Complex refactoring operations
│   │   ├── analysis_utils.py    # Helper functions for analysis
│   │   └── refactoring.py       # Basic refactoring operations
│   │
│   ├── parser/                   # Treesitter parsing layer
│   │   ├── java_parser.py       # Main parser wrapper for Treesitter
│   │   ├── node_navigator.py    # AST node traversal utilities
│   │   ├── query_engine.py      # Treesitter query execution
│   │   ├── query_patterns.py    # Predefined query patterns
│   │   └── edit_applier.py      # Edit application logic
│   │
│   ├── models/                   # Data models and schemas
│   │   ├── state.py             # LangGraph state definition
│   │   ├── edit.py              # Edit operation models
│   │   ├── position.py          # Position and range models
│   │   └── state_transitions.py # State transition definitions
│   │
│   ├── workflow/                 # LangGraph workflow definitions
│   │   ├── basic_workflow.py    # Standard parse-analyze-edit workflow
│   │   ├── refactoring_workflow.py  # Specialized refactoring workflows
│   │   ├── workflow_utils.py    # Workflow helper functions
│   │   └── checkpointer.py      # State checkpointing
│   │
│   ├── utils/                    # Utility functions
│   │   ├── edit_utils.py        # Edit manipulation helpers
│   │   ├── diff_utils.py        # Diff generation utilities
│   │   ├── java_validator.py   # Java code validation
│   │   ├── java_version.py      # Java version compatibility
│   │   └── state_utils.py       # State serialization
│   │
│   ├── optimization/             # Performance optimization
│   │   └── performance.py       # Caching and optimization
│   │
│   ├── config/                   # Configuration management
│   │   └── settings.py          # Application settings
│   │
│   └── main.py                   # CLI entry point
│
├── tests/                        # Test suite
│   ├── fixtures/                 # Test Java files
│   │   ├── simple.java          # Basic test cases
│   │   ├── Complex.java         # Complex code examples
│   │   └── integration/         # Integration test fixtures
│   │
│   ├── integration/              # Integration tests
│   │   ├── test_end_to_end.py   # Complete workflow tests
│   │   ├── test_error_recovery.py  # Error handling tests
│   │   └── test_java_features.py   # Java feature tests
│   │
│   ├── benchmarks/               # Performance benchmarks
│   │   ├── benchmark_parsing.py
│   │   ├── benchmark_workflow.py
│   │   └── benchmark_memory.py
│   │
│   └── test_*.py                 # Unit tests for each component
│
├── spec.md                       # Original specification document
├── prompt_plan.md                # Implementation plan
└── README.md                     # Project documentation
```

---

## Core Architecture

### Layered Architecture

The system is organized into distinct layers:

1. **Parser Layer** (`src/parser/`): Handles all Treesitter operations
2. **Model Layer** (`src/models/`): Defines data structures and state
3. **Agent Layer** (`src/agents/`): Implements LangGraph agents
4. **Workflow Layer** (`src/workflow/`): Orchestrates agent execution
5. **Utility Layer** (`src/utils/`): Provides helper functions

### Data Flow

```
Java Source Code
    ↓
Parser Agent (parse source → AST)
    ↓
Analyzer Agent (extract structure info)
    ↓
Editor Agent (generate modifications)
    ↓
Modified Java Source Code
```

---

## Treesitter Tree Construction

### How the Treesitter Tree is Built

The Treesitter tree is constructed through the following process:

#### 1. Parser Initialization (`JavaParser.__init__`)
**Location**: `src/parser/java_parser.py:14-22`

```python
def __init__(self):
    self.language = Language(tsjava.language())  # Load Java grammar
    self.parser = Parser(self.language)          # Create parser instance
    self.tree = None                              # Will store parsed tree
    self.navigator = NodeNavigator()              # For tree traversal
    self.query_engine = QueryEngine(self.language)  # For pattern matching
```

**What happens:**
- The Java language grammar is loaded from the `tree-sitter-java` package
- A parser instance is configured with this grammar
- Helper objects (navigator, query engine) are initialized for working with the tree

#### 2. Parsing Source Code (`JavaParser.parse`)
**Location**: `src/parser/java_parser.py:24-40`

```python
def parse(self, source_code: str) -> Tree:
    # Convert string to bytes (UTF-8 encoding)
    source_bytes = bytes(source_code, 'utf-8')

    # Parse and store the tree
    self.tree = self.parser.parse(source_bytes)

    return self.tree
```

**What happens:**
- Source code is converted to UTF-8 bytes (Treesitter works with byte offsets)
- The parser processes the bytes and builds an AST
- The resulting tree is stored for later access

#### 3. Tree Structure

The tree consists of nodes with the following properties:

- **type**: Node type (e.g., `class_declaration`, `method_declaration`)
- **start_byte/end_byte**: Byte positions in source
- **start_point/end_point**: (line, column) positions
- **children**: Child nodes in the AST
- **is_named**: Whether the node is a named syntax element
- **text**: The source text for this node

Example tree structure for `public class Hello {}`:

```
program
└── class_declaration
    ├── modifiers
    │   └── "public"
    ├── "class"
    ├── identifier: "Hello"
    └── class_body
        ├── "{"
        └── "}"
```

#### 4. Navigating the Tree (`NodeNavigator`)
**Location**: `src/parser/node_navigator.py`

The `NodeNavigator` class provides methods to traverse and query the tree:

- **`get_node_text(node, source_code)`**: Extract text for a node
- **`get_children(node)`**: Get all child nodes
- **`find_nodes_by_type(node, type)`**: Recursively find nodes of a specific type
- **`get_node_position(node)`**: Get (line, col) position

#### 5. Querying the Tree (`QueryEngine`)
**Location**: `src/parser/query_engine.py`

The query engine allows pattern matching using Treesitter query syntax:

```python
# Example query to find all methods
query = """
(method_declaration
  name: (identifier) @method.name
  parameters: (formal_parameters) @method.params
  body: (block) @method.body)
"""
results = query_engine.query_source(query, root_node, source_code)
```

**Predefined queries** are in `src/parser/query_patterns.py`:
- `find_methods`: Find all method declarations
- `find_classes`: Find all class declarations
- `find_fields`: Find all field declarations
- `find_constructors`: Find all constructors

---

## How Agents Use the Tree to Modify Code

### The Edit Pipeline

Agents use the Treesitter tree to modify code through a structured process:

#### Step 1: Parse the Code

**Agent**: `ParserAgent`
**Location**: `src/agents/parser_agent.py:18-73`

```python
def process(self, state: JavaCodeState) -> JavaCodeState:
    # Parse the source code
    tree = self.parser.parse(source)
    root_node = self.parser.get_root_node()

    # Update state with tree
    state['tree'] = tree
    state['root_node'] = root_node
```

#### Step 2: Analyze the Structure

**Agent**: `AnalyzerAgent`
**Location**: `src/agents/analyzer_agent.py:24-81`

```python
def process(self, state: JavaCodeState) -> JavaCodeState:
    # Use queries to find code elements
    classes = self._find_classes(root_node, source)
    methods = self._find_methods(root_node, source)
    fields = self._find_fields(root_node, source)

    # Store analysis results in state
    state['classes'] = classes
    state['methods'] = methods
    state['fields'] = fields
```

**What's stored in analysis results:**

For each **method**, the analyzer extracts:
- Name, return type, parameters
- Modifiers (public, static, etc.)
- Annotations
- Line range
- Full signature

For each **class**, the analyzer extracts:
- Name, modifiers, annotations
- Extends/implements clauses
- Generic type parameters
- Line range

#### Step 3: Generate Edit Operations

**Agent**: `EditorAgent`
**Location**: `src/agents/editor_agent.py`

The editor agent provides high-level operations that generate edit instructions:

**Example: Rename Method** (`editor_agent.py:105-166`)

```python
def rename_method(self, state: JavaCodeState, old_name: str, new_name: str):
    # Find method in analyzed state
    method = find_method_by_name(state['methods'], old_name)

    # Calculate byte positions from source
    byte_pos = calculate_byte_position(source, old_name)

    # Create a REPLACE edit
    edit = {
        'type': EditType.REPLACE,
        'start_pos': byte_pos,
        'end_pos': byte_pos + len(old_name.encode('utf-8')),
        'new_text': new_name,
        'description': f"Rename method {old_name} to {new_name}"
    }

    # Add to pending edits
    state['pending_edits'].append(edit)
```

**Example: Add Method** (`editor_agent.py:168-227`)

```python
def add_method(self, state: JavaCodeState, class_name: str, method_code: str):
    # Find class in analyzed state
    cls = find_class_by_name(state['classes'], class_name)

    # Determine insertion point (before closing brace)
    end_line = cls['line_range']['end_line']
    insertion_point = calculate_insertion_byte_position(source, end_line - 1)

    # Create an INSERT_BEFORE edit
    edit = {
        'type': EditType.INSERT_BEFORE,
        'start_pos': insertion_point,
        'end_pos': insertion_point,
        'new_text': f"\n    {method_code}\n",
        'description': f"Add method to class {class_name}"
    }

    state['pending_edits'].append(edit)
```

#### Step 4: Apply Edits

**Component**: `EditApplier`
**Location**: `src/parser/edit_applier.py:65-97`

```python
def apply_edits(self, source: str, edits: EditCollection) -> str:
    # Check for conflicts
    if edits.has_conflicts():
        raise ValueError("Cannot apply conflicting edits")

    # Sort edits in reverse order (end to beginning)
    # This ensures positions remain valid as we apply edits
    edits.sort_edits()

    # Apply each edit
    result = source
    for edit in edits:
        result = self.apply_single_edit(result, edit)

    return result
```

**Why reverse order?** If we apply edits from end to beginning, earlier byte positions remain valid even after modifications.

#### Step 5: Reparse the Modified Code

After edits are applied, the parser agent reparses the code to update the tree:

```python
def reparse_after_edit(self, state: JavaCodeState) -> JavaCodeState:
    # Parse the modified source
    state = self.parser_agent.process(state)

    # Re-extract basic info
    return self.parser_agent.extract_basic_info(state)
```

### Edit Types

**Location**: `src/models/edit.py:7-12`

```python
class EditType(Enum):
    INSERT_BEFORE = "insert_before"  # Insert text before position
    INSERT_AFTER = "insert_after"    # Insert text after position
    REPLACE = "replace"               # Replace text between positions
    DELETE = "delete"                 # Delete text between positions
```

### Conflict Detection

**Location**: `src/models/edit.py:44-55`

Edits are checked for conflicts (overlapping byte positions):

```python
def has_conflicts(self) -> bool:
    for i, edit1 in enumerate(self.edits):
        for edit2 in self.edits[i+1:]:
            if edits_overlap(edit1, edit2):
                return True
    return False
```

---

## Main Methods and Components

### JavaParser (`src/parser/java_parser.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `parse(source_code)` | Parse Java source into AST | Line 24 |
| `get_root_node()` | Get root node of parsed tree | Line 42 |
| `get_node_text(node, source)` | Extract text for a node | Line 53 |
| `find_nodes_by_type(node, type)` | Find all nodes of a type | Line 66 |
| `query(query_string, source)` | Execute Treesitter query | Line 91 |
| `apply_edits(source, edits)` | Apply modifications and reparse | Line 120 |

### NodeNavigator (`src/parser/node_navigator.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `get_node_text(node, source)` | Extract node text | Line 8 |
| `get_children(node)` | Get child nodes | Line 47 |
| `find_nodes_by_type(node, type)` | Recursively find nodes | Line 73 |
| `get_node_position(node)` | Get (line, col) position | Line 99 |
| `find_node_at_position(root, line, col)` | Find node at position | Line 152 |

### ParserAgent (`src/agents/parser_agent.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `process(state)` | Parse source and update state | Line 18 |
| `extract_basic_info(state)` | Extract package/imports | Line 75 |
| `validate_syntax(source)` | Quick syntax validation | Line 127 |

### AnalyzerAgent (`src/agents/analyzer_agent.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `process(state)` | Analyze code structure | Line 24 |
| `analyze_method(method_node, source)` | Extract method details | Line 83 |
| `analyze_class(class_node, source)` | Extract class details | Line 146 |
| `_find_methods(root_node, source)` | Find all methods | Line 254 |
| `_find_classes(root_node, source)` | Find all classes | Line 214 |
| `_find_fields(root_node, source)` | Find all fields | Line 338 |

### EditorAgent (`src/agents/editor_agent.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `process(state)` | Apply pending edits | Line 18 |
| `rename_method(state, old, new)` | Rename a method | Line 105 |
| `add_method(state, class, code)` | Add method to class | Line 168 |
| `delete_element(state, type, name)` | Delete code element | Line 229 |
| `add_import(state, import)` | Add import statement | Line 297 |

### JavaWorkflow (`src/workflow/basic_workflow.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `create_workflow()` | Build LangGraph workflow | Line 19 |
| `should_edit(state)` | Decide if editing needed | Line 54 |
| `reparse_after_edit(state)` | Reparse after modifications | Line 68 |

### StateManager (`src/models/state.py`)

**Primary methods:**

| Method | Purpose | Location |
|--------|---------|----------|
| `initialize_state(path, source)` | Create initial state | Line 48 |
| `update_state(state, updates)` | Update state immutably | Line 91 |
| `validate_state(state)` | Check state consistency | Line 133 |
| `save_checkpoint(state)` | Save state to history | Line 169 |
| `rollback_to_checkpoint(index)` | Restore previous state | Line 180 |

---

## Testing Approach

### Test Organization

Tests are organized by component and type:

```
tests/
├── test_parser.py              # JavaParser unit tests
├── test_navigator.py           # NodeNavigator unit tests
├── test_query_engine.py        # QueryEngine unit tests
├── test_edit_model.py          # Edit model tests
├── test_edit_applier.py        # Edit application tests
├── test_state.py               # State management tests
├── test_parser_agent.py        # Parser agent tests
├── test_analyzer_agent.py      # Analyzer agent tests
├── test_editor_agent.py        # Editor agent tests
├── test_basic_workflow.py      # Workflow tests
├── test_java_patterns.py       # Pattern recognition tests
├── test_advanced_refactoring.py  # Advanced refactoring tests
├── integration/                # Integration tests
│   ├── test_end_to_end.py
│   ├── test_error_recovery.py
│   └── test_java_features.py
└── benchmarks/                 # Performance tests
    ├── benchmark_parsing.py
    ├── benchmark_workflow.py
    └── benchmark_memory.py
```

### Running Tests

**With uv (recommended):**
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src tests/

# Run specific test file
uv run pytest tests/test_parser.py

# Run integration tests only
uv run pytest tests/integration/

# Run with verbose output
uv run pytest -v
```

**With pip/venv:**
```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest
pytest --cov=src tests/
```

### Test Structure

Tests follow a consistent pattern:

```python
class TestComponentName:
    def setup_method(self):
        """Set up test fixtures before each test"""
        self.component = Component()

    def test_basic_functionality(self):
        """Test description"""
        # Arrange
        input_data = create_test_data()

        # Act
        result = self.component.process(input_data)

        # Assert
        assert result.is_valid()
        assert result.output == expected_output
```

### Integration Test Example

**Location**: `tests/integration/test_end_to_end.py:22-47`

```python
def test_rename_method_scenario(self):
    """Test complete method renaming workflow"""
    # Load Java file
    fixture_path = Path('tests/fixtures/integration/Project.java')
    source = fixture_path.read_text()

    # Initialize state
    state = self.state_manager.initialize_state('Project.java', source)

    # Run initial parsing and analysis
    state = self.workflow.invoke(state)

    # Verify method was found
    method_names = [m['name'] for m in state.get('methods', [])]
    assert 'processData' in method_names

    # Add rename edit using editor agent
    state = self.editor.rename_method(state, 'processData', 'handleData')

    # Run workflow to apply edit
    result = self.workflow.invoke(state)

    # Verify method renamed
    assert 'handleData' in result['current_source']
    assert 'processData' not in result['current_source']
    assert len(result['applied_edits']) > 0
```

---

## Adding New Examples

### Adding Test Fixtures

Test fixtures are Java files used for testing. They are located in `tests/fixtures/`.

#### Step 1: Create the Java File

Create a new `.java` file in the appropriate directory:

```bash
# For simple examples
tests/fixtures/YourExample.java

# For integration tests
tests/fixtures/integration/YourIntegration.java
```

#### Step 2: Write Valid Java Code

```java
package com.example;

public class YourExample {
    private String field;

    public YourExample(String field) {
        this.field = field;
    }

    public String getField() {
        return field;
    }
}
```

#### Step 3: Create a Test

Create or update a test file to use your fixture:

```python
def test_your_example():
    """Test with YourExample.java fixture"""
    # Load fixture
    fixture_path = Path('tests/fixtures/YourExample.java')
    source = fixture_path.read_text()

    # Initialize state
    state_manager = StateManager()
    state = state_manager.initialize_state('YourExample.java', source)

    # Create workflow
    workflow_obj = JavaWorkflow()
    workflow = workflow_obj.create_workflow()

    # Run workflow
    result = workflow.invoke(state)

    # Verify results
    assert len(result['classes']) == 1
    assert result['classes'][0]['name'] == 'YourExample'
```

#### Step 4: Run the Test

```bash
uv run pytest tests/test_your_example.py -v
```

### Adding New Query Patterns

**Location**: `src/parser/query_patterns.py`

Add a new query to the `QUERIES` dictionary:

```python
QUERIES = {
    # ... existing queries ...

    "find_lambda_expressions": """
        (lambda_expression
          parameters: (inferred_parameters) @lambda.params
          body: (_) @lambda.body)
    """,
}
```

Use the query in your code:

```python
query_engine = QueryEngine(language)
results = query_engine.query_source(
    QUERIES['find_lambda_expressions'],
    root_node,
    source_code
)
```

### Adding New Refactoring Operations

**Location**: `src/agents/editor_agent.py` or `src/agents/java_refactoring.py`

Add a new method to the `EditorAgent` or refactoring classes:

```python
def extract_variable(self, state: JavaCodeState,
                     expression: str, variable_name: str) -> JavaCodeState:
    """Extract an expression into a local variable"""
    # 1. Find the expression in the source
    # 2. Generate variable declaration
    # 3. Create edits to:
    #    - Insert variable declaration
    #    - Replace expression with variable name
    # 4. Add edits to pending_edits

    return state
```

### Adding Integration Test Scenarios

**Location**: `tests/integration/test_end_to_end.py`

Add a new test method:

```python
def test_your_refactoring_scenario(self):
    """Test your specific refactoring scenario"""
    # 1. Load or create source code
    source = """..."""

    # 2. Initialize state
    state = self.state_manager.initialize_state('Test.java', source)

    # 3. Perform refactoring operations
    state = self.editor.your_operation(state, params)

    # 4. Run workflow
    result = self.workflow.invoke(state)

    # 5. Verify expected changes
    assert 'expected_result' in result['current_source']
```

---

## Workflow Execution

### The Basic Workflow

The basic workflow follows this sequence:

```
Start
  ↓
Parse (ParserAgent)
  ↓
Extract Info (ParserAgent)
  ↓
Analyze (AnalyzerAgent)
  ↓
Should Edit? ──No──→ End
  ↓ Yes
Edit (EditorAgent)
  ↓
Reparse (ParserAgent)
  ↓
(back to Analyze)
```

### Workflow State

**Location**: `src/models/state.py:5-39`

The workflow state contains:

```python
class JavaCodeState(TypedDict):
    # File information
    file_path: str                    # Path to Java file
    original_source: str              # Original source code
    current_source: str               # Current (possibly modified) source

    # Parsing state
    tree: Optional[Any]               # Treesitter Tree object
    root_node: Optional[Any]          # Root AST node
    parse_errors: List[str]           # Any parse errors

    # Analysis results
    classes: List[Dict]               # Found classes
    methods: List[Dict]               # Found methods
    fields: List[Dict]                # Found fields
    imports: List[str]                # Import statements
    package: Optional[str]            # Package declaration

    # Edit state
    pending_edits: List[Dict]         # Edits to apply
    applied_edits: List[Dict]         # History of applied edits
    edit_conflicts: List[Dict]        # Detected conflicts

    # Workflow state
    current_step: str                 # Current workflow step
    completed_steps: List[str]        # Completed steps
    errors: List[str]                 # Error messages
    warnings: List[str]               # Warning messages
```

### Creating a Workflow

**Location**: `src/workflow/basic_workflow.py:19-52`

```python
def create_workflow(self):
    workflow = StateGraph(JavaCodeState)

    # Add nodes (agents)
    workflow.add_node("parse", self.parser_agent.process)
    workflow.add_node("extract_info", self.parser_agent.extract_basic_info)
    workflow.add_node("analyze", self.analyzer_agent.process)
    workflow.add_node("edit", self.editor_agent.process)
    workflow.add_node("reparse", self.reparse_after_edit)

    # Add edges (flow)
    workflow.add_edge("parse", "extract_info")
    workflow.add_edge("extract_info", "analyze")
    workflow.add_conditional_edges(
        "analyze",
        self.should_edit,  # Decision function
        {
            "edit": "edit",
            "end": END
        }
    )
    workflow.add_edge("edit", "reparse")
    workflow.add_edge("reparse", "analyze")

    # Set entry point
    workflow.set_entry_point("parse")

    return workflow.compile()
```

### Executing a Workflow

```python
# Create workflow
workflow_obj = JavaWorkflow()
workflow = workflow_obj.create_workflow()

# Initialize state
state_manager = StateManager()
state = state_manager.initialize_state('Example.java', source_code)

# Execute workflow
result = workflow.invoke(state)

# Access results
print(f"Classes found: {len(result['classes'])}")
print(f"Methods found: {len(result['methods'])}")
print(f"Modified source:\n{result['current_source']}")
```

---

## Common Use Cases

### 1. Rename a Method

```python
from src.workflow.basic_workflow import JavaWorkflow
from src.models.state import StateManager
from src.agents.editor_agent import EditorAgent

# Load Java source
source = """
public class Example {
    public void oldMethod() {
        System.out.println("Hello");
    }
}
"""

# Initialize
state_manager = StateManager()
editor = EditorAgent()
workflow_obj = JavaWorkflow()

# Create workflow and state
workflow = workflow_obj.create_workflow()
state = state_manager.initialize_state('Example.java', source)

# Add rename operation
state = editor.rename_method(state, 'oldMethod', 'newMethod')

# Execute workflow
result = workflow.invoke(state)

print(result['current_source'])
# Output:
# public class Example {
#     public void newMethod() {
#         System.out.println("Hello");
#     }
# }
```

### 2. Add a Method to a Class

```python
# Add method operation
method_code = """
public String getName() {
    return name;
}
""".strip()

state = editor.add_method(state, 'Example', method_code)

# Execute workflow
result = workflow.invoke(state)
```

### 3. Analyze Java Code

```python
# Just analyze without editing
state = state_manager.initialize_state('Example.java', source)
result = workflow.invoke(state)

# Access analysis results
for method in result['methods']:
    print(f"Method: {method['name']}")
    print(f"  Return type: {method['return_type']}")
    print(f"  Parameters: {method['parameters']}")
    print(f"  Modifiers: {method['modifiers']}")
```

### 4. Using the CLI

The system provides a command-line interface:

```bash
# Analyze a file
uv run python -m src.main Example.java --operation analyze

# Rename a method
uv run python -m src.main Example.java \
    --operation rename \
    --old-name oldMethod \
    --new-name newMethod \
    --output Example_modified.java

# Interactive mode
uv run python -m src.main Example.java --interactive
```

### 5. Batch Operations

```python
# Queue multiple edits
state = editor.rename_method(state, 'method1', 'newMethod1')
state = editor.add_import(state, 'java.util.List')
state = editor.add_method(state, 'Example', getter_code)

# All edits applied in one workflow execution
result = workflow.invoke(state)
```

---

## Key Concepts

### Immutability

The state is updated immutably - each update creates a new state object:

```python
new_state = state_manager.update_state(state, {'current_step': 'parsed'})
```

### Checkpointing

States can be saved and restored:

```python
# Save checkpoint
state_manager.save_checkpoint(state)

# Later, rollback
previous_state = state_manager.rollback_to_checkpoint()
```

### Error Handling

Agents handle errors gracefully:

```python
try:
    # Perform operation
    result = process(state)
except Exception as e:
    # Add error to state, optionally rollback
    state = state_manager.add_error(state, str(e))
```

### Byte Positions

All edit positions use byte offsets (not character positions) to handle Unicode correctly:

```python
source_bytes = source.encode('utf-8')
start_byte = node.start_byte
end_byte = node.end_byte
text = source_bytes[start_byte:end_byte].decode('utf-8')
```

---

## Advanced Topics

### Custom Queries

Write Treesitter queries to find specific patterns:

```python
# Find all static methods
query = """
(method_declaration
  (modifiers "static")
  name: (identifier) @static.method)
"""

results = query_engine.query_source(query, root_node, source)
```

### Pattern Recognition

The system can identify common Java patterns:

```python
from src.agents.java_patterns import JavaPatternHandler

pattern_handler = JavaPatternHandler()

# Identify getter/setter methods
getters_setters = pattern_handler.identify_getter_setter(state)

# Identify design patterns
singleton = pattern_handler.identify_singleton(state)
builder = pattern_handler.identify_builder_pattern(state)
```

### Performance Optimization

The system includes caching for better performance:

```python
from src.optimization.performance import PerformanceOptimizer

optimizer = PerformanceOptimizer()

# Cache frequently used queries
optimizer.cache_query(QUERIES['find_methods'])

# Cache parse trees
optimizer.cache_parse_tree(file_hash, tree)
```

---

## Conclusion

This Java AST Agent system provides a powerful, extensible framework for Java code analysis and refactoring. By combining Treesitter's fast parsing with LangGraph's agent-based workflows, it enables complex code transformations while maintaining code validity and structure.

### Key Strengths

- **Fast parsing**: Treesitter is highly optimized
- **Accurate**: Works with the actual syntax tree
- **Extensible**: Easy to add new agents and operations
- **Safe**: Validates edits and handles conflicts
- **Testable**: Comprehensive test coverage

### Getting Started

1. Install dependencies: `uv sync`
2. Run tests: `uv run pytest`
3. Try the CLI: `uv run python -m src.main tests/fixtures/simple.java --operation analyze`
4. Explore the code starting with `src/parser/java_parser.py`
5. Read the tests to understand usage patterns

For more details, see:
- `README.md` - Installation and usage
- `spec.md` - Original specification
- `prompt_plan.md` - Implementation plan
