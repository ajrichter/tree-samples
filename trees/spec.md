# Treesitter Java Implementation for LangGraph Agent Pipeline

## Executive Summary

This specification outlines the requirements and implementation details for migrating a Python AST-based code editing pipeline to support Java files using Treesitter as the parsing backend, integrated with LangGraph agents running in Python.

## 1. System Overview

### 1.1 Current State
- **Technology**: Python-based LangGraph agents
- **Capability**: Parse and edit Python files via AST manipulation
- **Architecture**: Agent-based pipeline for code understanding and modification

### 1.2 Target State
- **Technology**: Python-based LangGraph agents with Treesitter Java support
- **Capability**: Parse and edit Java files with full syntax awareness
- **Architecture**: Maintain agent-based pipeline, extend to Java language support

## 2. Core Components

### 2.1 Treesitter Integration

#### 2.1.1 Python Bindings
```python
# Required packages
py-tree-sitter >= 0.20.0
tree-sitter-java >= 0.20.0
```

#### 2.1.2 Parser Initialization
```python
from tree_sitter import Language, Parser
import tree_sitter_java as tsjava

# Build the Java language library
JAVA_LANGUAGE = Language(tsjava.language(), 'java')

# Initialize parser
parser = Parser()
parser.set_language(JAVA_LANGUAGE)
```

### 2.2 Java AST Node Types

#### 2.2.1 Essential Node Types to Support
- **Compilation Unit**: Root node for Java files
- **Package Declaration**: `package_declaration`
- **Import Declarations**: `import_declaration`
- **Class/Interface**: `class_declaration`, `interface_declaration`
- **Methods**: `method_declaration`, `constructor_declaration`
- **Fields**: `field_declaration`
- **Statements**: All statement types (if, while, for, try-catch, etc.)
- **Expressions**: All expression types
- **Annotations**: `annotation`, `marker_annotation`, `annotation_argument_list`
- **Modifiers**: `modifiers` (public, private, static, final, etc.)
- **Type Parameters**: Generic type support

#### 2.2.2 Query Patterns
```scheme
; Example Treesitter queries for Java
(method_declaration
  name: (identifier) @method.name
  parameters: (formal_parameters) @method.params
  body: (block) @method.body)

(class_declaration
  name: (identifier) @class.name
  body: (class_body) @class.body)
```

## 3. Agent Architecture

### 3.1 LangGraph Agent Structure

#### 3.1.1 State Definition
```python
from typing import TypedDict, List, Optional, Any
from langgraph.graph import StateGraph

class JavaCodeState(TypedDict):
    file_path: str
    source_code: str
    tree: Optional[Any]  # Treesitter tree object
    cursor: Optional[Any]  # Treesitter cursor
    edits: List[dict]  # Pending edits
    analysis_results: dict
    error_messages: List[str]
```

#### 3.1.2 Agent Nodes
1. **Parser Node**: Parse Java source into Treesitter AST
2. **Analyzer Node**: Analyze code structure and patterns
3. **Navigator Node**: Navigate and query the AST
4. **Editor Node**: Generate code modifications
5. **Validator Node**: Validate Java syntax and semantics
6. **Formatter Node**: Format modified code

### 3.2 Core Agent Functions

#### 3.2.1 Parsing Agent
```python
def parse_java_code(state: JavaCodeState) -> JavaCodeState:
    """Parse Java source code into Treesitter AST"""
    parser = Parser()
    parser.set_language(JAVA_LANGUAGE)
    tree = parser.parse(bytes(state['source_code'], 'utf8'))
    state['tree'] = tree
    state['cursor'] = tree.walk()
    return state
```

#### 3.2.2 Query Agent
```python
def query_java_ast(state: JavaCodeState, query: str) -> JavaCodeState:
    """Execute Treesitter queries on Java AST"""
    query_obj = JAVA_LANGUAGE.query(query)
    captures = query_obj.captures(state['tree'].root_node)
    state['analysis_results']['query_results'] = captures
    return state
```

## 4. Java-Specific Features

### 4.1 Type Resolution
- **Requirement**: Resolve Java types including generics
- **Implementation**: Build symbol table from AST
- **Considerations**: Handle imports, nested classes, type parameters

### 4.2 Scope Analysis
- **Package Scope**: Track package-level declarations
- **Class Scope**: Handle inner classes, static members
- **Method Scope**: Local variables, parameters, closures
- **Block Scope**: Variables in blocks, loops, conditionals

### 4.3 Java-Specific Patterns
- **Annotations Processing**: Parse and modify annotations
- **Lambda Expressions**: Handle Java 8+ lambdas
- **Stream API**: Recognize and modify stream operations
- **Records**: Support Java 14+ records
- **Pattern Matching**: Support modern Java pattern matching

## 5. Edit Operations

### 5.1 Basic Edit Operations
```python
class JavaEditOperation:
    def __init__(self, operation_type: str, node: Any, **kwargs):
        self.type = operation_type  # insert, delete, replace, move
        self.node = node
        self.params = kwargs
```

### 5.2 Complex Refactoring Operations
1. **Method Extraction**: Extract code into new method
2. **Variable Renaming**: Rename with scope awareness
3. **Class Restructuring**: Add/remove fields, methods
4. **Interface Implementation**: Auto-implement interfaces
5. **Generic Type Addition**: Add type parameters
6. **Annotation Modification**: Add/remove/modify annotations

## 6. Implementation Requirements

### 6.1 Dependencies
```python
# requirements.txt
langgraph>=0.0.20
langchain>=0.1.0
tree-sitter>=0.20.0
tree-sitter-java>=0.20.0
typing-extensions>=4.0.0
pydantic>=2.0.0
```

### 6.2 Project Structure
```
project/
├── agents/
│   ├── __init__.py
│   ├── parser_agent.py
│   ├── analyzer_agent.py
│   ├── editor_agent.py
│   ├── validator_agent.py
│   └── formatter_agent.py
├── treesitter/
│   ├── __init__.py
│   ├── java_parser.py
│   ├── queries.py
│   └── node_types.py
├── models/
│   ├── __init__.py
│   ├── java_ast.py
│   └── edit_operations.py
├── utils/
│   ├── __init__.py
│   ├── java_utils.py
│   └── ast_utils.py
└── tests/
    ├── test_parser.py
    ├── test_agents.py
    └── fixtures/
```

## 7. Key Interfaces

### 7.1 Parser Interface
```python
class JavaParser:
    def parse(self, source: str) -> Tree
    def query(self, tree: Tree, query: str) -> List[Capture]
    def get_node_text(self, node: Node) -> str
    def get_node_type(self, node: Node) -> str
```

### 7.2 Editor Interface
```python
class JavaEditor:
    def insert_before(self, node: Node, text: str) -> Edit
    def insert_after(self, node: Node, text: str) -> Edit
    def replace_node(self, node: Node, text: str) -> Edit
    def delete_node(self, node: Node) -> Edit
    def apply_edits(self, source: str, edits: List[Edit]) -> str
```

### 7.3 Agent Interface
```python
class JavaAgent:
    def process(self, state: JavaCodeState) -> JavaCodeState
    def validate(self, state: JavaCodeState) -> bool
    def get_capabilities(self) -> List[str]
```

## 8. Migration Strategy

### 8.1 Phase 1: Core Infrastructure
1. Set up Treesitter Java parser
2. Create basic AST navigation utilities
3. Implement simple edit operations
4. Build initial LangGraph agent structure

### 8.2 Phase 2: Feature Parity
1. Map Python AST operations to Java equivalents
2. Implement Java-specific node handlers
3. Create comprehensive test suite
4. Validate against real Java codebases

### 8.3 Phase 3: Java-Specific Enhancements
1. Add Java-specific refactoring operations
2. Implement type resolution system
3. Add support for modern Java features
4. Optimize performance for large files

## 9. Testing Requirements

### 9.1 Unit Tests
- Parser functionality for all Java constructs
- Individual agent node testing
- Edit operation validation
- Query pattern correctness

### 9.2 Integration Tests
- Full pipeline execution
- Multi-file project handling
- Complex refactoring scenarios
- Edge cases and error handling

### 9.3 Test Coverage Targets
- Node type coverage: 100% of supported Java nodes
- Edit operations: All CRUD operations
- Agent paths: All possible state transitions
- Java versions: Java 8 through Java 21

## 10. Performance Considerations

### 10.1 Optimization Points
- **Parsing**: Cache parsed trees for unchanged files
- **Queries**: Precompile frequently used queries
- **Edits**: Batch edit operations when possible
- **Memory**: Implement tree cleanup for large projects

### 10.2 Benchmarks
- Parse time: < 100ms for 1000 LOC file
- Query execution: < 10ms for simple queries
- Edit application: < 50ms for batch edits
- Memory usage: < 100MB for 10k LOC project

## 11. Error Handling

### 11.1 Parse Errors
- Graceful handling of syntax errors
- Partial tree recovery
- Error location reporting

### 11.2 Edit Conflicts
- Detect overlapping edits
- Resolve or report conflicts
- Maintain code validity

## 12. Example Implementation

### 12.1 Simple Method Renaming Agent
```python
from langgraph.graph import StateGraph, END

def create_method_rename_graph():
    workflow = StateGraph(JavaCodeState)
    
    # Add nodes
    workflow.add_node("parse", parse_java_code)
    workflow.add_node("find_method", find_method_node)
    workflow.add_node("rename", rename_method_node)
    workflow.add_node("validate", validate_java_syntax)
    workflow.add_node("format", format_java_code)
    
    # Add edges
    workflow.add_edge("parse", "find_method")
    workflow.add_edge("find_method", "rename")
    workflow.add_edge("rename", "validate")
    workflow.add_edge("validate", "format")
    workflow.add_edge("format", END)
    
    # Set entry point
    workflow.set_entry_point("parse")
    
    return workflow.compile()
```

## 13. Deliverables

### 13.1 Core Components
1. Treesitter Java parser wrapper
2. LangGraph agent implementation
3. Edit operation library
4. Query pattern library

### 13.2 Documentation
1. API documentation
2. Usage examples
3. Migration guide from Python
4. Performance tuning guide

### 13.3 Tools
1. CLI for testing agents
2. Visualization for AST
3. Diff viewer for edits
4. Benchmark suite

## 14. Success Criteria

1. **Functional**: Successfully parse and edit Java files
2. **Compatible**: Maintain compatibility with existing pipeline
3. **Performant**: Meet or exceed performance benchmarks
4. **Reliable**: 99%+ success rate on valid Java code
5. **Maintainable**: Clear architecture and documentation

## 15. Future Enhancements

1. **Multi-language Support**: Extend to other languages
2. **AI Integration**: LLM-powered code understanding
3. **IDE Integration**: Plugin for popular IDEs
4. **Cloud Deployment**: Scalable cloud-based processing
5. **Real-time Collaboration**: Multi-user editing support

## Appendix A: Treesitter Query Examples

```scheme
; Find all public methods
(method_declaration
  (modifiers "public")
  name: (identifier) @method.public)

; Find all class fields
(field_declaration
  declarator: (variable_declarator
    name: (identifier) @field.name))

; Find all try-catch blocks
(try_statement
  body: (block) @try.body
  (catch_clause
    parameter: (catch_formal_parameter) @catch.param
    body: (block) @catch.body))
```

## Appendix B: Common Java AST Patterns

```python
# Common patterns to recognize
PATTERNS = {
    "getter_method": """
        (method_declaration
          (modifiers "public")
          type: (_) @return.type
          name: (identifier) @method.name
          parameters: (formal_parameters)
          body: (block
            (return_statement
              (field_access) @field)))
    """,
    "setter_method": """
        (method_declaration
          (modifiers "public")
          type: (void_type)
          name: (identifier) @method.name
          parameters: (formal_parameters
            (formal_parameter) @param)
          body: (block
            (expression_statement
              (assignment_expression))))
    """,
}
```

## Appendix C: References

1. [Treesitter Documentation](https://tree-sitter.github.io/tree-sitter/)
2. [Treesitter Java Grammar](https://github.com/tree-sitter/tree-sitter-java)
3. [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
4. [Java Language Specification](https://docs.oracle.com/javase/specs/)
5. [Python Tree-sitter Bindings](https://github.com/tree-sitter/py-tree-sitter)
