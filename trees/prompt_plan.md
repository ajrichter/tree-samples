# Implementation Blueprint: Treesitter Java LangGraph Agent

## Phase 1: Initial Blueprint

### High-Level Architecture
1. **Foundation Layer**: Project setup, dependencies, basic infrastructure
2. **Parser Layer**: Treesitter integration, AST parsing, node navigation
3. **Query Layer**: Pattern matching, node selection, AST queries
4. **Edit Layer**: Modification operations, text manipulation, edit application
5. **Agent Layer**: LangGraph agents, state management, workflow orchestration
6. **Java Layer**: Language-specific features, refactoring operations
7. **Integration Layer**: End-to-end pipeline, testing, optimization

## Phase 2: First Iteration - Major Chunks

### Chunk 1: Core Infrastructure (Days 1-2)
- Project structure setup
- Dependency management
- Treesitter Java parser initialization
- Basic test framework

### Chunk 2: AST Operations (Days 3-4)
- Node navigation utilities
- Query system implementation
- Text extraction and manipulation
- Basic edit operations

### Chunk 3: Agent Framework (Days 5-6)
- State management schema
- Individual agent implementations
- Agent communication protocols
- Error handling

### Chunk 4: Workflow Integration (Days 7-8)
- LangGraph workflow setup
- Agent orchestration
- End-to-end pipeline
- Integration testing

### Chunk 5: Java Specialization (Days 9-10)
- Java-specific patterns
- Complex refactoring
- Performance optimization
- Production readiness

## Phase 3: Second Iteration - Detailed Steps

### Foundation Steps (1-4)
1. **Project Initialization**: Directory structure, virtual environment, git setup
2. **Dependency Installation**: tree-sitter, py-tree-sitter, tree-sitter-java, langgraph
3. **Parser Setup**: Initialize Treesitter with Java language support
4. **Verification**: Test parser with simple Java file

### Parsing Steps (5-8)
5. **AST Navigation**: Walk tree, extract nodes, get text
6. **Query Basics**: Write and execute simple queries
7. **Query Patterns**: Method, class, field queries
8. **Query Results**: Capture processing and result extraction

### Edit Steps (9-12)
9. **Edit Structures**: Define Edit class, position tracking
10. **Edit Operations**: Insert, delete, replace implementations
11. **Edit Application**: Apply single and batch edits
12. **Edit Validation**: Conflict detection, order resolution

### State Steps (13-16)
13. **State Definition**: TypedDict schema for JavaCodeState
14. **State Operations**: Initialize, update, validate
15. **State Persistence**: Serialization, history tracking
16. **State Transitions**: Legal transitions, error states

### Agent Steps (17-20)
17. **Parser Agent**: Parse source to AST with error handling
18. **Analyzer Agent**: Extract code structure information
19. **Editor Agent**: Generate and apply modifications
20. **Validator Agent**: Syntax and semantic validation

### Workflow Steps (21-24)
21. **Graph Definition**: Create LangGraph workflow structure
22. **Node Connection**: Wire agents with edges
23. **Flow Control**: Conditional routing, error paths
24. **Compilation**: Build executable workflow

### Integration Steps (25-28)
25. **Basic Pipeline**: Parse → Analyze → Edit flow
26. **Testing Suite**: Unit and integration tests
27. **Error Handling**: Graceful failures, recovery
28. **Performance**: Optimization and benchmarking

## Phase 4: Third Iteration - Right-Sized Implementation Steps

After careful review, here are the optimally-sized steps that balance safety with progress:

### Stage 1: Minimal Viable Parser (Steps 1-3)
1. **Setup & Dependencies**: Project structure + core dependencies + verification
2. **Parser Wrapper**: Treesitter initialization + parse function + basic test
3. **Node Utilities**: Node traversal + text extraction + type identification

### Stage 2: Query System (Steps 4-6)
4. **Query Engine**: Query compilation + execution + capture extraction
5. **Pattern Library**: Common Java patterns + method/class/field queries
6. **Query Testing**: Query validation + result verification + edge cases

### Stage 3: Edit System (Steps 7-9)
7. **Edit Model**: Edit class + position tracking + conflict detection
8. **Edit Operations**: CRUD operations + batch processing + ordering
9. **Edit Application**: Source modification + rollback support + testing

### Stage 4: State Management (Steps 10-12)
10. **State Schema**: TypedDict definition + initialization + validation
11. **State Transitions**: Update logic + history + error handling
12. **State Testing**: State validation + transition testing + persistence

### Stage 5: Core Agents (Steps 13-15)
13. **Parser Agent**: Parsing logic + error handling + state update
14. **Analyzer Agent**: Structure extraction + pattern matching + results storage
15. **Editor Agent**: Edit generation + application + state synchronization

### Stage 6: Workflow (Steps 16-18)
16. **Graph Construction**: Node definition + edge connections + entry point
17. **Flow Execution**: Run pipeline + handle results + error paths
18. **Integration Tests**: End-to-end testing + multi-step validation

### Stage 7: Java Features (Steps 19-21)
19. **Java Patterns**: Getters/setters + constructors + annotations
20. **Refactoring Ops**: Method extraction + renaming + restructuring
21. **Final Integration**: Complete pipeline + optimization + documentation

## Phase 5: Implementation Prompts for Code-Generation LLM

Below are the carefully crafted prompts for implementing each step in a test-driven manner:

---

## Prompt 1: Project Setup and Dependencies ✅ COMPLETED

```text
Create a Python project structure for a Treesitter-based Java code analysis system that will run as LangGraph agents. 

Requirements:
1. Create the following directory structure:
   - src/
     - __init__.py
     - parser/
       - __init__.py
     - agents/
       - __init__.py
     - models/
       - __init__.py
     - utils/
       - __init__.py
   - tests/
     - __init__.py
     - fixtures/
       - simple.java (containing a basic HelloWorld class)
   - requirements.txt
   - setup.py
   - README.md

2. Create requirements.txt with:
   - tree-sitter>=0.20.0
   - tree-sitter-java>=0.20.0  
   - langgraph>=0.0.20
   - langchain>=0.1.0
   - pydantic>=2.0.0
   - pytest>=7.0.0
   - pytest-cov>=4.0.0

3. Create a setup.py that installs the package as 'java-ast-agent'

4. Create tests/test_setup.py that:
   - Tests that tree-sitter can be imported
   - Tests that tree-sitter-java can be imported
   - Tests that langgraph can be imported
   - Verifies the fixture file exists and is valid Java

5. Create a simple HelloWorld.java fixture in tests/fixtures/:
   ```java
   public class HelloWorld {
       public static void main(String[] args) {
           System.out.println("Hello, World!");
       }
   }
   ```

Run pytest to ensure all imports work correctly. This establishes our foundation.
```

---

## Prompt 2: Basic Treesitter Parser Wrapper ✅ COMPLETED

```text
Building on the project structure from Prompt 1, create a basic Treesitter parser wrapper for Java.

Requirements:
1. Create src/parser/java_parser.py with:
   - A JavaParser class that:
     - Initializes the tree-sitter Parser with Java language
     - Has a parse() method that takes Java source code and returns a tree
     - Has a get_root_node() method that returns the root AST node
     - Handles encoding properly (UTF-8)
   
2. The class should:
   ```python
   class JavaParser:
       def __init__(self):
           # Initialize parser with Java language
       
       def parse(self, source_code: str):
           # Parse source code and return tree
           
       def get_root_node(self):
           # Return root node of last parsed tree
   ```

3. Create tests/test_parser.py that:
   - Tests parsing the HelloWorld.java fixture
   - Verifies the root node type is "program"
   - Tests parsing invalid Java code raises appropriate errors
   - Tests parsing empty string
   - Tests that get_root_node() returns None before parsing
   - Tests that get_root_node() returns correct node after parsing

4. Ensure the parser:
   - Properly handles the tree-sitter-java language building
   - Stores the tree for later access
   - Handles UTF-8 encoding correctly

Run pytest to verify the parser works correctly. This gives us basic parsing capability.
```

---

## Prompt 3: AST Node Navigation Utilities ✅ COMPLETED

```text
Building on the parser from Prompt 2, add AST node navigation utilities.

Requirements:
1. Create src/parser/node_navigator.py with:
   - A NodeNavigator class that provides methods for traversing the AST:
     ```python
     class NodeNavigator:
         def get_node_text(self, node, source_code: str) -> str:
             # Extract text content of a node
             
         def get_node_type(self, node) -> str:
             # Get the type of a node
             
         def get_children(self, node) -> list:
             # Get all children of a node
             
         def find_nodes_by_type(self, node, node_type: str) -> list:
             # Recursively find all nodes of a specific type
             
         def get_node_position(self, node) -> tuple:
             # Return (start_line, start_col, end_line, end_col)
     ```

2. Create tests/test_navigator.py that:
   - Parses HelloWorld.java and tests:
     - Finding the class declaration node
     - Finding the method declaration node  
     - Extracting text from the main method
     - Getting positions of various nodes
     - Finding all identifier nodes
   - Tests with a more complex Java fixture (create Complex.java):
     ```java
     package com.example;
     import java.util.*;
     
     public class Complex {
         private String field;
         
         public Complex(String field) {
             this.field = field;
         }
         
         public String getField() {
             return field;
         }
     }
     ```

3. Integrate NodeNavigator with JavaParser:
   - JavaParser should have a navigator property
   - Add convenience methods to JavaParser that delegate to navigator

Run pytest to verify navigation works. This completes our basic AST traversal capability.
```

---

## Prompt 4: Query System Implementation ✅ COMPLETED

```text
Building on the navigation utilities from Prompt 3, implement a Treesitter query system.

Requirements:
1. Create src/parser/query_engine.py with:
   ```python
   class QueryEngine:
       def __init__(self, java_language):
           # Store the language object for query compilation
           
       def compile_query(self, query_string: str):
           # Compile a tree-sitter query string
           
       def execute_query(self, query, root_node) -> list:
           # Execute query and return captures
           
       def extract_captures(self, captures, source_code: str) -> dict:
           # Convert captures to readable format with text
   ```

2. Create src/parser/query_patterns.py with common Java queries:
   ```python
   QUERIES = {
       "find_methods": """
           (method_declaration
             name: (identifier) @method.name
             parameters: (formal_parameters) @method.params
             body: (block) @method.body)
       """,
       "find_classes": """
           (class_declaration
             name: (identifier) @class.name
             body: (class_body) @class.body)
       """,
       "find_fields": """
           (field_declaration
             declarator: (variable_declarator
               name: (identifier) @field.name))
       """,
       "find_constructors": """
           (constructor_declaration
             name: (identifier) @constructor.name
             parameters: (formal_parameters) @constructor.params)
       """
   }
   ```

3. Create tests/test_query_engine.py that:
   - Tests each query pattern on Complex.java
   - Verifies correct capture extraction
   - Tests malformed query handling
   - Tests query with no matches
   - Validates capture positions and text

4. Integrate QueryEngine with JavaParser:
   - Add query methods to JavaParser
   - Cache compiled queries for performance

Run pytest to verify the query system works. This enables pattern-based code analysis.
```

---

## Prompt 5: Edit Model and Data Structures ✅ COMPLETED

```text
Building on previous components, create the edit system data structures.

Requirements:
1. Create src/models/edit.py with:
   ```python
   from dataclasses import dataclass
   from enum import Enum
   from typing import Optional
   
   class EditType(Enum):
       INSERT_BEFORE = "insert_before"
       INSERT_AFTER = "insert_after"
       REPLACE = "replace"
       DELETE = "delete"
   
   @dataclass
   class Edit:
       type: EditType
       start_pos: int  # byte position
       end_pos: int    # byte position
       new_text: str
       description: str
       
       def to_dict(self) -> dict:
           # Convert to dictionary
           
   class EditCollection:
       def __init__(self):
           self.edits = []
           
       def add_edit(self, edit: Edit):
           # Add edit and check for conflicts
           
       def sort_edits(self):
           # Sort edits by position (reverse for safe application)
           
       def has_conflicts(self) -> bool:
           # Check if any edits overlap
           
       def get_conflicts(self) -> list:
           # Return list of conflicting edit pairs
   ```

2. Create src/models/position.py with:
   ```python
   @dataclass
   class Position:
       line: int
       column: int
       byte_offset: int
       
   @dataclass  
   class Range:
       start: Position
       end: Position
       
       def overlaps_with(self, other: 'Range') -> bool:
           # Check if ranges overlap
   ```

3. Create tests/test_edit_model.py that:
   - Tests Edit creation and serialization
   - Tests EditCollection conflict detection
   - Tests edit sorting for safe application order
   - Tests position/range overlap detection
   - Tests with various edit combinations

4. Create helper functions in src/utils/edit_utils.py:
   - node_to_range(node) -> Range
   - position_from_point(point) -> Position
   - validate_edit(edit, source_length) -> bool

Run pytest to verify edit structures work correctly. This provides our modification framework.
```

---

## Prompt 6: Edit Application Logic ✅ COMPLETED

```text
Building on the edit model from Prompt 5, implement edit application logic.

Requirements:
1. Create src/parser/edit_applier.py with:
   ```python
   class EditApplier:
       def __init__(self):
           pass
           
       def apply_single_edit(self, source: str, edit: Edit) -> str:
           # Apply one edit to source code
           
       def apply_edits(self, source: str, edits: EditCollection) -> str:
           # Apply multiple edits safely
           # Must handle overlapping edits
           # Must apply in correct order
           
       def preview_edit(self, source: str, edit: Edit) -> str:
           # Show what would change without applying
           
       def calculate_line_changes(self, source: str, edit: Edit) -> dict:
           # Return lines added/removed/modified
   ```

2. Create tests/test_edit_applier.py that:
   - Tests single edit application (all types)
   - Tests multiple non-overlapping edits
   - Tests handling of conflicting edits
   - Tests edit preview functionality
   - Tests with Complex.java:
     - Replace method name
     - Insert new field
     - Delete a method
     - Insert import statement

3. Integrate with JavaParser:
   - Add apply_edits() method to JavaParser
   - Ensure tree is re-parsed after edits
   - Maintain edit history

4. Create src/utils/diff_utils.py:
   - generate_diff(original, modified) -> str
   - highlight_changes(original, modified) -> str

Run pytest to ensure edit application works correctly. This completes our modification capability.
```

---

## Prompt 7: State Schema Definition ✅ COMPLETED

```text
Building on previous components, define the state schema for LangGraph agents.

Requirements:
1. Create src/models/state.py with:
   ```python
   from typing import TypedDict, List, Optional, Any, Dict
   from pydantic import BaseModel, Field
   
   class JavaCodeState(TypedDict):
       # File information
       file_path: str
       original_source: str
       current_source: str
       
       # Parsing state
       tree: Optional[Any]  # tree-sitter Tree object
       root_node: Optional[Any]  # root Node
       parse_errors: List[str]
       
       # Analysis results
       classes: List[Dict]  # Found classes
       methods: List[Dict]  # Found methods  
       fields: List[Dict]   # Found fields
       imports: List[str]   # Import statements
       package: Optional[str]  # Package declaration
       
       # Edit state
       pending_edits: List[Dict]  # Edits to apply
       applied_edits: List[Dict]  # History of applied edits
       edit_conflicts: List[Dict]  # Detected conflicts
       
       # Workflow state
       current_step: str
       completed_steps: List[str]
       errors: List[str]
       warnings: List[str]
   
   class StateManager:
       def __init__(self):
           self.state_history = []
           
       def initialize_state(self, file_path: str, source: str) -> JavaCodeState:
           # Create initial state
           
       def update_state(self, state: JavaCodeState, updates: dict) -> JavaCodeState:
           # Update state immutably
           
       def validate_state(self, state: JavaCodeState) -> bool:
           # Check state consistency
           
       def save_checkpoint(self, state: JavaCodeState):
           # Save state to history
           
       def rollback_to_checkpoint(self, index: int) -> JavaCodeState:
           # Restore previous state
   ```

2. Create tests/test_state.py that:
   - Tests state initialization with HelloWorld.java
   - Tests state updates maintain immutability
   - Tests state validation catches inconsistencies
   - Tests checkpoint/rollback functionality
   - Tests state transitions are tracked correctly

3. Create src/models/state_transitions.py:
   - Define valid state transitions
   - Create transition validator
   - Add transition logging

4. Add state serialization in src/utils/state_utils.py:
   - serialize_state(state) -> dict
   - deserialize_state(data) -> JavaCodeState
   - state_to_json(state) -> str

Run pytest to verify state management works. This provides our workflow foundation.
```

---

## Prompt 8: Parser Agent Implementation ✅ COMPLETED

```text
Building on the state schema from Prompt 7, create the first LangGraph agent.

Requirements:
1. Create src/agents/parser_agent.py with:
   ```python
   from typing import Dict, Any
   from src.models.state import JavaCodeState
   from src.parser.java_parser import JavaParser
   from src.parser.node_navigator import NodeNavigator
   
   class ParserAgent:
       def __init__(self):
           self.parser = JavaParser()
           self.navigator = NodeNavigator()
           
       def process(self, state: JavaCodeState) -> JavaCodeState:
           """Parse Java source and update state with AST"""
           try:
               # Parse the current source
               # Update tree and root_node in state
               # Clear any parse errors if successful
               # Mark step as completed
           except Exception as e:
               # Add error to state
               # Set parse_errors
           return state
           
       def extract_basic_info(self, state: JavaCodeState) -> JavaCodeState:
           """Extract package and imports from parsed tree"""
           # Use navigator to find package declaration
           # Find all import statements
           # Update state with findings
           return state
           
       def validate_syntax(self, source: str) -> Dict[str, Any]:
           """Quick syntax validation without full state update"""
           # Parse and return validation results
   ```

2. Create tests/test_parser_agent.py that:
   - Tests parsing valid Java updates state correctly
   - Tests parsing invalid Java captures errors
   - Tests package/import extraction
   - Tests with multiple Java fixtures:
     ```java
     // NoPackage.java - test file without package
     public class NoPackage {
         void method() {}
     }
     
     // Errors.java - test file with syntax errors  
     public class Errors {
         void broken() {
             // Missing closing brace
     }
     ```

3. Create agent utilities in src/agents/base_agent.py:
   ```python
   class BaseAgent:
       def pre_process(self, state):
           # Common pre-processing
       def post_process(self, state):
           # Common post-processing
       def handle_error(self, state, error):
           # Standard error handling
   ```

4. Add logging to parser agent for debugging

Run pytest to ensure the parser agent works correctly. This is our first working agent.
```

---

## Prompt 9: Analyzer Agent Implementation ✅ COMPLETED

```text
Building on the parser agent from Prompt 8, create the analyzer agent.

Requirements:
1. Create src/agents/analyzer_agent.py with:
   ```python
   from src.models.state import JavaCodeState
   from src.parser.query_engine import QueryEngine
   from src.parser.query_patterns import QUERIES
   
   class AnalyzerAgent:
       def __init__(self):
           self.query_engine = None
           
       def process(self, state: JavaCodeState) -> JavaCodeState:
           """Analyze code structure using queries"""
           if not state.get('root_node'):
               state['errors'].append("No parsed tree available")
               return state
               
           try:
               # Initialize query engine if needed
               # Find all classes
               # Find all methods with details
               # Find all fields with types
               # Find constructors
               # Update state with analysis results
           except Exception as e:
               # Handle errors
           return state
           
       def analyze_method(self, method_node, source: str) -> dict:
           """Extract detailed method information"""
           # Get method name, parameters, return type
           # Get modifiers (public, static, etc.)
           # Get line numbers
           # Check for annotations
           
       def analyze_class(self, class_node, source: str) -> dict:
           """Extract detailed class information"""
           # Get class name, modifiers
           # Check for extends/implements
           # Get class-level annotations
           
       def analyze_relationships(self, state: JavaCodeState) -> JavaCodeState:
           """Analyze relationships between code elements"""
           # Find method calls
           # Find field usage
           # Build dependency graph
   ```

2. Create tests/test_analyzer_agent.py with:
   - Test analyzing Complex.java structure
   - Test with a richer fixture (create Analyzer.java):
     ```java
     package com.test;
     
     import java.util.List;
     import java.util.ArrayList;
     
     @Deprecated
     public class Analyzer extends BaseClass implements Interface1 {
         private static final String CONSTANT = "test";
         private List<String> items;
         
         @Override
         public void method1(String param1, int param2) {
             // Method implementation
         }
         
         protected static List<String> method2() throws Exception {
             return new ArrayList<>();
         }
     }
     ```
   - Verify all elements are found and categorized correctly
   - Test relationship analysis

3. Create src/agents/analysis_utils.py:
   - extract_modifiers(node) -> List[str]
   - extract_annotations(node) -> List[dict]
   - extract_generic_types(node) -> dict
   - build_signature(method_node) -> str

Run pytest to verify analyzer works. This provides code understanding capability.
```

---

## Prompt 10: Editor Agent Implementation ✅ COMPLETED

```text
Building on previous agents, create the editor agent for code modifications.

Requirements:
1. Create src/agents/editor_agent.py with:
   ```python
   from src.models.state import JavaCodeState
   from src.models.edit import Edit, EditType, EditCollection
   from src.parser.edit_applier import EditApplier
   
   class EditorAgent:
       def __init__(self):
           self.edit_applier = EditApplier()
           
       def process(self, state: JavaCodeState) -> JavaCodeState:
           """Apply pending edits to source code"""
           if not state.get('pending_edits'):
               return state
               
           try:
               # Convert pending_edits to EditCollection
               # Check for conflicts
               # Apply edits to current_source
               # Update state with new source
               # Move edits to applied_edits
               # Clear pending_edits
               # Request re-parse
           except Exception as e:
               # Handle errors
           return state
           
       def rename_method(self, state: JavaCodeState, old_name: str, new_name: str) -> JavaCodeState:
           """Generate edits to rename a method"""
           # Find method in state['methods']
           # Create replace edit
           # Add to pending_edits
           
       def add_method(self, state: JavaCodeState, class_name: str, method_code: str) -> JavaCodeState:
           """Generate edit to add new method to class"""
           # Find class body
           # Determine insertion point
           # Create insert edit
           
       def delete_element(self, state: JavaCodeState, element_type: str, element_name: str) -> JavaCodeState:
           """Generate edit to delete a code element"""
           # Find element (method, field, etc.)
           # Create delete edit
           
       def add_import(self, state: JavaCodeState, import_statement: str) -> JavaCodeState:
           """Add import statement to file"""
           # Find import section or create one
           # Create appropriate insert edit
   ```

2. Create tests/test_editor_agent.py that:
   - Test renaming methods in HelloWorld.java
   - Test adding new method to Complex.java
   - Test deleting elements
   - Test adding imports (both to existing and new import sections)
   - Test edit conflict handling
   - Test batch operations

3. Create src/agents/refactoring.py with higher-level operations:
   ```python
   class RefactoringOperations:
       def extract_method(self, state, start_line, end_line, method_name):
           # Extract code block into new method
           
       def inline_variable(self, state, var_name):
           # Replace variable with its value
           
       def generate_getters_setters(self, state, class_name):
           # Generate accessor methods for fields
   ```

4. Add edit validation in src/utils/java_validator.py:
   - validate_method_name(name) -> bool
   - validate_class_name(name) -> bool  
   - validate_java_syntax(code) -> bool

Run pytest to verify editor agent works. This enables code modification capability.
```

---

## Prompt 11: Basic LangGraph Workflow ✅ COMPLETED

```text
Connect all agents into a working LangGraph workflow.

Requirements:
1. Create src/workflow/basic_workflow.py with:
   ```python
   from langgraph.graph import StateGraph, END
   from src.models.state import JavaCodeState
   from src.agents.parser_agent import ParserAgent
   from src.agents.analyzer_agent import AnalyzerAgent
   from src.agents.editor_agent import EditorAgent
   
   class JavaWorkflow:
       def __init__(self):
           self.parser_agent = ParserAgent()
           self.analyzer_agent = AnalyzerAgent()
           self.editor_agent = EditorAgent()
           
       def create_workflow(self):
           workflow = StateGraph(JavaCodeState)
           
           # Add nodes
           workflow.add_node("parse", self.parser_agent.process)
           workflow.add_node("extract_info", self.parser_agent.extract_basic_info)
           workflow.add_node("analyze", self.analyzer_agent.process)
           workflow.add_node("edit", self.editor_agent.process)
           workflow.add_node("reparse", self.reparse_after_edit)
           
           # Add edges
           workflow.add_edge("parse", "extract_info")
           workflow.add_edge("extract_info", "analyze")
           workflow.add_conditional_edges(
               "analyze",
               self.should_edit,
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
           
       def should_edit(self, state: JavaCodeState) -> str:
           """Decide whether to proceed to edit"""
           if state.get('pending_edits'):
               return "edit"
           return "end"
           
       def reparse_after_edit(self, state: JavaCodeState) -> JavaCodeState:
           """Reparse after edits are applied"""
           # Update state to trigger reparse
           state['current_step'] = 'reparse'
           return self.parser_agent.process(state)
   ```

2. Create tests/test_basic_workflow.py that:
   - Tests parse-only workflow (no edits)
   - Tests parse-analyze-edit-reparse cycle
   - Tests workflow with multiple edit rounds
   - Tests error handling in workflow
   - Test with a practical scenario:
     ```python
     # Test renaming a method
     state = initialize_state("Complex.java", source)
     state['pending_edits'] = [rename_method_edit]
     result = workflow.invoke(state)
     assert "getField" not in result['current_source']
     assert "getNewName" in result['current_source']
     ```

3. Create src/workflow/workflow_utils.py:
   - create_simple_workflow() -> compiled workflow
   - create_refactoring_workflow() -> compiled workflow
   - visualize_workflow(workflow) -> graphviz output

4. Add checkpointing in src/workflow/checkpointer.py:
   - Implement workflow state checkpointing
   - Add rollback capability

Run pytest to verify the workflow executes correctly. This creates our functioning pipeline.
```

---

## Prompt 12: Integration Testing Suite ✅ COMPLETED

```text
Create comprehensive integration tests for the complete system.

Requirements:
1. Create tests/integration/test_end_to_end.py with:
   ```python
   class TestEndToEnd:
       def test_rename_method_scenario(self):
           """Test complete method renaming workflow"""
           # Load Java file
           # Initialize workflow
           # Add rename edit
           # Run workflow
           # Verify method renamed
           # Verify code still compiles (conceptually)
           
       def test_add_getter_setter_scenario(self):
           """Test adding accessor methods"""
           # Start with class with private field
           # Generate getter/setter
           # Apply through workflow
           # Verify methods added correctly
           
       def test_extract_method_scenario(self):
           """Test extracting code into new method"""
           # Select code block
           # Extract to method
           # Verify extraction and call insertion
           
       def test_multi_file_refactoring(self):
           """Test refactoring across multiple files"""
           # Load multiple related Java files
           # Perform interconnected refactoring
           # Verify consistency across files
   ```

2. Create test fixtures in tests/fixtures/integration/:
   ```java
   // Project.java - A complete small project
   package com.example.project;
   
   public class Project {
       private Database db;
       private Logger logger;
       
       public void processData(String input) {
           // Complex method to be refactored
           logger.log("Starting process");
           String cleaned = input.trim().toLowerCase();
           if (cleaned.isEmpty()) {
               logger.error("Empty input");
               return;
           }
           Data data = parseData(cleaned);
           db.save(data);
           logger.log("Process complete");
       }
   }
   ```

3. Create tests/integration/test_error_recovery.py:
   - Test workflow recovery from parse errors
   - Test handling of conflicting edits
   - Test rollback on validation failure
   - Test partial success scenarios

4. Create performance benchmarks in tests/benchmarks/:
   - benchmark_parsing.py - Parse speed for various file sizes
   - benchmark_workflow.py - Full workflow execution time
   - benchmark_memory.py - Memory usage profiling

5. Create tests/integration/test_java_features.py:
   - Test with Java 8 features (lambdas, streams)
   - Test with generics
   - Test with annotations
   - Test with inner classes

Run full test suite to ensure system works end-to-end. This validates our implementation.
```

---

## Prompt 13: Java-Specific Pattern Handlers ✅ COMPLETED

```text
Add specialized handlers for Java-specific code patterns.

Requirements:
1. Create src/agents/java_patterns.py with:
   ```python
   class JavaPatternHandler:
       def identify_getter_setter(self, state: JavaCodeState) -> dict:
           """Identify getter/setter methods"""
           # Match getter pattern: public Type getX()
           # Match setter pattern: public void setX(Type x)
           # Link to corresponding fields
           
       def identify_builder_pattern(self, state: JavaCodeState) -> dict:
           """Identify builder pattern implementation"""
           # Find builder class
           # Find fluent methods
           # Find build() method
           
       def identify_singleton(self, state: JavaCodeState) -> dict:
           """Identify singleton pattern"""
           # Private constructor
           # Static instance field
           # GetInstance method
           
       def analyze_annotations(self, state: JavaCodeState) -> dict:
           """Process Java annotations"""
           # Find all annotations
           # Extract parameters
           # Categorize (Spring, JPA, etc.)
           
       def handle_generics(self, node, source: str) -> dict:
           """Extract generic type information"""
           # Parse type parameters
           # Handle bounded types
           # Process wildcards
   ```

2. Create src/agents/java_refactoring.py:
   ```python
   class JavaRefactoringAgent:
       def generate_equals_hashcode(self, state: JavaCodeState, class_name: str):
           """Generate equals() and hashCode() methods"""
           # Analyze fields
           # Generate appropriate methods
           # Handle null checks
           
       def implement_interface(self, state: JavaCodeState, class_name: str, interface_name: str):
           """Auto-implement interface methods"""
           # Parse interface requirements
           # Generate method stubs
           # Add implements clause
           
       def convert_to_lambda(self, state: JavaCodeState, anonymous_class_node):
           """Convert anonymous class to lambda"""
           # Check if functional interface
           # Extract single method
           # Convert to lambda syntax
           
       def add_try_with_resources(self, state: JavaCodeState, resource_usage_node):
           """Wrap resource usage in try-with-resources"""
           # Identify resource
           # Wrap in try block
           # Remove explicit close()
   ```

3. Create tests/test_java_patterns.py with comprehensive tests:
   - Test pattern identification on real Java code
   - Test refactoring operations
   - Test with various Java versions
   - Create fixtures with different patterns:
     ```java
     // PatternExamples.java
     public class PatternExamples {
         // Singleton pattern
         private static PatternExamples instance;
         private PatternExamples() {}
         
         public static PatternExamples getInstance() {
             if (instance == null) {
                 instance = new PatternExamples();
             }
             return instance;
         }
         
         // Builder pattern inner class
         public static class Builder {
             private String field1;
             
             public Builder withField1(String field1) {
                 this.field1 = field1;
                 return this;
             }
             
             public PatternExamples build() {
                 return new PatternExamples();
             }
         }
     }
     ```

4. Create Java version compatibility in src/utils/java_version.py:
   - detect_java_version(source) -> int
   - is_feature_available(version, feature) -> bool
   - get_version_warnings(source, target_version) -> list

Run tests to ensure Java patterns work correctly. This adds language-specific intelligence.
```

---

## Prompt 14: Advanced Refactoring Operations ✅ COMPLETED

```text
Implement complex refactoring operations that modify code structure.

Requirements:
1. Create src/agents/advanced_refactoring.py with:
   ```python
   class AdvancedRefactoringAgent:
       def extract_method(self, state: JavaCodeState, start_line: int, end_line: int, 
                         method_name: str, parameters: list = None):
           """Extract code block into a new method"""
           # Analyze selected code
           # Identify variables needed as parameters
           # Identify return values
           # Generate new method
           # Replace original code with method call
           
       def extract_class(self, state: JavaCodeState, methods: list, fields: list, 
                        class_name: str):
           """Extract methods and fields into new class"""
           # Create new class
           # Move specified members
           # Update references
           # Handle dependencies
           
       def inline_method(self, state: JavaCodeState, method_name: str):
           """Replace method calls with method body"""
           # Find all calls to method
           # Get method body
           # Replace calls with body
           # Handle parameters
           # Remove method definition
           
       def pull_up_method(self, state: JavaCodeState, method_name: str, 
                          target_class: str):
           """Move method to parent class"""
           # Verify inheritance relationship
           # Check method compatibility
           # Move method
           # Update access modifiers
           
       def convert_to_strategy_pattern(self, state: JavaCodeState, 
                                       switch_statement_node):
           """Convert switch to strategy pattern"""
           # Analyze switch cases
           # Create strategy interface
           # Create concrete strategies
           # Replace switch with strategy usage
   ```

2. Create src/workflow/refactoring_workflow.py:
   ```python
   class RefactoringWorkflow:
       def create_extract_method_workflow(self):
           """Specialized workflow for method extraction"""
           workflow = StateGraph(JavaCodeState)
           
           # Add analysis phase
           workflow.add_node("analyze_selection", self.analyze_code_selection)
           workflow.add_node("identify_variables", self.identify_variable_usage)
           workflow.add_node("generate_signature", self.generate_method_signature)
           workflow.add_node("create_method", self.create_new_method)
           workflow.add_node("replace_code", self.replace_with_call)
           workflow.add_node("validate_refactoring", self.validate_result)
           
           # Connect nodes with conditional edges
           # Handle edge cases and errors
           
           return workflow.compile()
   ```

3. Create comprehensive tests in tests/test_advanced_refactoring.py:
   - Test method extraction with various scenarios:
     - No parameters, no return
     - Multiple parameters
     - Return value
     - Multiple return paths
     - Exception handling
   - Test class extraction
   - Test pattern conversions

4. Create fixture with refactoring opportunities:
   ```java
   // RefactorMe.java
   public class RefactorMe {
       public void longMethod() {
           // Setup code
           String data = loadData();
           validate(data);
           
           // Processing code (extract this)
           String[] parts = data.split(",");
           for (String part : parts) {
               part = part.trim();
               if (part.length() > 0) {
                   process(part);
               }
           }
           
           // Cleanup code
           cleanup();
       }
       
       public String processType(int type) {
           // Convert to strategy pattern
           switch(type) {
               case 1:
                   return "Type A processing";
               case 2:
                   return "Type B processing";
               case 3:
                   return "Type C processing";
               default:
                   return "Unknown type";
           }
       }
   }
   ```

Run tests to verify advanced refactoring works. This enables structural modifications.
```

---

## Prompt 15: Final Integration and Optimization ✅ COMPLETED

```text
Complete the system with final integration, optimization, and production readiness.

Requirements:
1. Create src/main.py as the main entry point:
   ```python
   from typing import Optional
   import argparse
   from pathlib import Path
   
   class JavaRefactorCLI:
       def __init__(self):
           self.workflow_factory = WorkflowFactory()
           
       def run(self, args):
           """Main execution entry point"""
           # Parse command line arguments
           # Load Java file(s)
           # Select workflow based on operation
           # Execute workflow
           # Output results
           
       def interactive_mode(self):
           """Interactive refactoring mode"""
           # Present menu of operations
           # Guide user through refactoring
           # Preview changes
           # Confirm and apply
           
   def main():
       parser = argparse.ArgumentParser()
       parser.add_argument('file', help='Java file to process')
       parser.add_argument('--operation', choices=['rename', 'extract', 'analyze'])
       parser.add_argument('--interactive', action='store_true')
       # Add more arguments
       
       args = parser.parse_args()
       cli = JavaRefactorCLI()
       cli.run(args)
   ```

2. Create src/optimization/performance.py:
   ```python
   class PerformanceOptimizer:
       def __init__(self):
           self.query_cache = {}
           self.parse_cache = {}
           
       def cache_query(self, query_string: str):
           """Pre-compile and cache frequently used queries"""
           
       def cache_parse_tree(self, file_hash: str, tree):
           """Cache parse trees for unchanged files"""
           
       def batch_operations(self, operations: list):
           """Batch similar operations for efficiency"""
           
       def parallel_analysis(self, files: list):
           """Analyze multiple files in parallel"""
   ```

3. Create src/config/settings.py for configuration:
   ```python
   from pydantic import BaseSettings
   
   class Settings(BaseSettings):
       max_file_size: int = 1_000_000  # bytes
       enable_caching: bool = True
       parallel_processing: bool = False
       java_version: int = 11
       strict_mode: bool = False
       
       class Config:
           env_file = ".env"
   ```

4. Create comprehensive documentation:
   - docs/API.md - Complete API reference
   - docs/TUTORIAL.md - Step-by-step usage guide
   - docs/PATTERNS.md - Supported Java patterns
   - docs/PERFORMANCE.md - Performance tuning guide

5. Create tests/test_production.py:
   - Test with large real-world Java files
   - Test with complete Java projects
   - Test performance benchmarks
   - Test error recovery and logging
   - Test with various Java frameworks (Spring, etc.)

6. Create Docker support:
   - Dockerfile for containerized deployment
   - docker-compose.yml for development
   - CI/CD configuration (.github/workflows/ci.yml)

7. Final integration test with real project:
   ```python
   def test_real_world_project():
       """Test with actual open-source Java project"""
       # Clone a real Java project
       # Run various refactoring operations
       # Verify code still compiles
       # Measure performance metrics
   ```

Run final test suite and benchmarks. Package for distribution. This completes the implementation.
```

---

## Summary

This blueprint provides a comprehensive, test-driven approach to building a Treesitter-based Java analysis and refactoring system using LangGraph agents. Each prompt:

1. **Builds on previous work** - No orphaned code
2. **Includes comprehensive tests** - Test-driven development
3. **Adds specific functionality** - Clear, focused goals
4. **Integrates immediately** - Everything connects
5. **Maintains production quality** - Error handling, logging, documentation

The progression ensures:
- **Early testing** - Parser works before agents
- **Incremental complexity** - Simple edits before refactoring
- **Strong foundation** - State management before workflows  
- **Complete integration** - All pieces connect in the workflow
- **Production readiness** - Performance, errors, real-world testing

Each prompt can be given to an LLM to generate working, tested code that builds into a complete system.
