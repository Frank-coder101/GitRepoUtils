"""
ExtP Indexing System - Build comprehensive searchable index of ExtP components
"""

import os
import json
import sqlite3
import hashlib
import ast
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class IndexedItem:
    """Represents an indexed item from ExtP"""
    id: str
    type: str  # 'function', 'class', 'config', 'requirement', 'menu', 'prompt', 'state_var'
    name: str
    source_file: str
    line_number: int
    content: str
    context: str
    metadata: Dict[str, Any]
    hash: str
    last_modified: str

class ExtPIndexer:
    """Comprehensive indexing system for ExtP analysis"""
    
    def __init__(self, extP_path: str, cache_path: str = "extP_index.db"):
        self.extP_path = Path(extP_path)
        self.cache_path = cache_path
        self.db_connection = None
        self.initialize_database()
    
    def initialize_database(self):
        """Initialize SQLite database for indexing"""
        self.db_connection = sqlite3.connect(self.cache_path)
        cursor = self.db_connection.cursor()
        
        # Create main index table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extP_index (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                name TEXT NOT NULL,
                source_file TEXT NOT NULL,
                line_number INTEGER,
                content TEXT,
                context TEXT,
                metadata TEXT,  -- JSON blob
                hash TEXT NOT NULL,
                last_modified TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create indexes for fast searching
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_type ON extP_index(type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON extP_index(name)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source_file ON extP_index(source_file)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_hash ON extP_index(hash)')
        
        # Create relationships table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_item_id TEXT NOT NULL,
                to_item_id TEXT NOT NULL,
                relationship_type TEXT NOT NULL,  -- 'calls', 'imports', 'configures', 'validates'
                metadata TEXT,
                FOREIGN KEY (from_item_id) REFERENCES extP_index(id),
                FOREIGN KEY (to_item_id) REFERENCES extP_index(id)
            )
        ''')
        
        # Create change tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS change_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL,
                change_type TEXT NOT NULL,  -- 'added', 'modified', 'deleted'
                old_hash TEXT,
                new_hash TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (item_id) REFERENCES extP_index(id)
            )
        ''')
        
        self.db_connection.commit()
    
    def build_full_index(self) -> Dict[str, int]:
        """Build complete index of ExtP system"""
        print(f"Building comprehensive index of {self.extP_path}")
        
        stats = {
            'functions': 0,
            'classes': 0,
            'configs': 0,
            'requirements': 0,
            'menus': 0,
            'prompts': 0,
            'state_vars': 0,
            'files_processed': 0
        }
        
        # Index source code files
        for py_file in self.extP_path.rglob("*.py"):
            self._index_python_file(py_file, stats)
        
        # Index configuration files
        for config_file in self.extP_path.rglob("*.json"):
            self._index_config_file(config_file, stats)
        
        # Index documentation
        for doc_file in self.extP_path.rglob("*.md"):
            self._index_documentation_file(doc_file, stats)
        
        # Index other relevant files
        for txt_file in self.extP_path.rglob("*.txt"):
            self._index_text_file(txt_file, stats)
        
        # Build relationships
        self._build_relationships()
        
        print(f"Indexing complete: {stats}")
        return stats
    
    def _index_python_file(self, file_path: Path, stats: Dict[str, int]):
        """Index a Python source file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for structural analysis
            tree = ast.parse(content, filename=str(file_path))
            
            # Index functions
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._index_function(node, file_path, content, stats)
                elif isinstance(node, ast.ClassDef):
                    self._index_class(node, file_path, content, stats)
                elif isinstance(node, ast.Assign):
                    self._index_variable_assignment(node, file_path, content, stats)
            
            # Index UI prompts and menus
            self._index_ui_elements(content, file_path, stats)
            
            stats['files_processed'] += 1
            
        except Exception as e:
            print(f"Error indexing {file_path}: {e}")
    
    def _index_function(self, node: ast.FunctionDef, file_path: Path, content: str, stats: Dict[str, int]):
        """Index a function definition"""
        lines = content.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 10
        
        function_content = '\n'.join(lines[start_line:end_line])
        context = '\n'.join(lines[max(0, start_line-3):min(len(lines), end_line+3)])
        
        metadata = {
            'args': [arg.arg for arg in node.args.args],
            'docstring': ast.get_docstring(node),
            'decorators': [self._get_decorator_name(d) for d in node.decorator_list],
            'complexity': self._calculate_complexity(node)
        }
        
        item = IndexedItem(
            id=self._generate_id('function', file_path, node.name, node.lineno),
            type='function',
            name=node.name,
            source_file=str(file_path.relative_to(self.extP_path)),
            line_number=node.lineno,
            content=function_content,
            context=context,
            metadata=metadata,
            hash=self._calculate_hash(function_content),
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        )
        
        self._store_item(item)
        stats['functions'] += 1
    
    def _index_class(self, node: ast.ClassDef, file_path: Path, content: str, stats: Dict[str, int]):
        """Index a class definition"""
        lines = content.split('\n')
        start_line = node.lineno - 1
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line + 20
        
        class_content = '\n'.join(lines[start_line:end_line])
        
        metadata = {
            'bases': [self._get_base_name(base) for base in node.bases],
            'methods': [n.name for n in node.body if isinstance(n, ast.FunctionDef)],
            'docstring': ast.get_docstring(node)
        }
        
        item = IndexedItem(
            id=self._generate_id('class', file_path, node.name, node.lineno),
            type='class',
            name=node.name,
            source_file=str(file_path.relative_to(self.extP_path)),
            line_number=node.lineno,
            content=class_content,
            context=class_content,
            metadata=metadata,
            hash=self._calculate_hash(class_content),
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        )
        
        self._store_item(item)
        stats['classes'] += 1
    
    def _index_ui_elements(self, content: str, file_path: Path, stats: Dict[str, int]):
        """Index UI prompts, menus, and user interactions"""
        lines = content.split('\n')
        
        # Patterns for different UI elements
        patterns = {
            'menu': [
                r'print\s*\(\s*["\'].*(?:menu|option|choice|select).*["\']',
                r'print\s*\(\s*["\'].*\d+[\.\)]\s*.*["\']',  # Numbered options
            ],
            'prompt': [
                r'input\s*\(\s*["\'].*["\']',
                r'print\s*\(\s*["\'].*(?:enter|input|type).*["\']',
            ],
            'config': [
                r'[A-Z_]+\s*=\s*.*',  # Configuration constants
                r'config\[.*\]',
                r'\.config\.',
            ]
        }
        
        for line_num, line in enumerate(lines, 1):
            for element_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        self._index_ui_element(
                            element_type, match.group(), file_path, 
                            line_num, line, stats
                        )
    
    def _index_ui_element(self, element_type: str, match_text: str, file_path: Path, 
                         line_num: int, line_context: str, stats: Dict[str, int]):
        """Index a UI element (menu, prompt, etc.)"""
        
        # Extract meaningful text from the match
        clean_text = re.sub(r'["\']', '', match_text).strip()
        
        metadata = {
            'pattern_matched': match_text,
            'context_line': line_context.strip(),
            'element_category': element_type
        }
        
        item = IndexedItem(
            id=self._generate_id(element_type, file_path, clean_text, line_num),
            type=element_type,
            name=clean_text[:100],  # Truncate long names
            source_file=str(file_path.relative_to(self.extP_path)),
            line_number=line_num,
            content=match_text,
            context=line_context,
            metadata=metadata,
            hash=self._calculate_hash(match_text),
            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        )
        
        self._store_item(item)
        if element_type in stats:
            stats[element_type] += 1
    
    def _index_config_file(self, file_path: Path, stats: Dict[str, int]):
        """Index configuration files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                config_data = json.loads(content)
            
            # Index each configuration item
            for key, value in self._flatten_config(config_data).items():
                item = IndexedItem(
                    id=self._generate_id('config', file_path, key, 0),
                    type='config',
                    name=key,
                    source_file=str(file_path.relative_to(self.extP_path)),
                    line_number=0,
                    content=json.dumps({key: value}, indent=2),
                    context=content[:500],  # First 500 chars of file
                    metadata={'value_type': type(value).__name__, 'file_type': 'json'},
                    hash=self._calculate_hash(str(value)),
                    last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                )
                
                self._store_item(item)
                stats['configs'] += 1
                
        except Exception as e:
            print(f"Error indexing config file {file_path}: {e}")
    
    def _index_documentation_file(self, file_path: Path, stats: Dict[str, int]):
        """Index markdown documentation files"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract requirements from markdown
            requirements = self._extract_requirements(content)
            
            for req_id, req_text in requirements.items():
                item = IndexedItem(
                    id=self._generate_id('requirement', file_path, req_id, 0),
                    type='requirement',
                    name=req_id,
                    source_file=str(file_path.relative_to(self.extP_path)),
                    line_number=0,
                    content=req_text,
                    context=content[:1000],
                    metadata={'file_type': 'markdown', 'requirement_id': req_id},
                    hash=self._calculate_hash(req_text),
                    last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                )
                
                self._store_item(item)
                stats['requirements'] += 1
                
        except Exception as e:
            print(f"Error indexing documentation {file_path}: {e}")
    
    def query_index(self, query_type: str = None, name_pattern: str = None, 
                   file_pattern: str = None, content_search: str = None) -> List[IndexedItem]:
        """Query the index with various filters"""
        cursor = self.db_connection.cursor()
        
        where_clauses = []
        params = []
        
        if query_type:
            where_clauses.append("type = ?")
            params.append(query_type)
        
        if name_pattern:
            where_clauses.append("name LIKE ?")
            params.append(f"%{name_pattern}%")
        
        if file_pattern:
            where_clauses.append("source_file LIKE ?")
            params.append(f"%{file_pattern}%")
        
        if content_search:
            where_clauses.append("content LIKE ?")
            params.append(f"%{content_search}%")
        
        where_clause = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        query = f"""
            SELECT id, type, name, source_file, line_number, content, context, metadata, hash, last_modified
            FROM extP_index 
            WHERE {where_clause}
            ORDER BY type, source_file, line_number
        """
        
        cursor.execute(query, params)
        results = []
        
        for row in cursor.fetchall():
            metadata = json.loads(row[7]) if row[7] else {}
            item = IndexedItem(
                id=row[0], type=row[1], name=row[2], source_file=row[3],
                line_number=row[4], content=row[5], context=row[6],
                metadata=metadata, hash=row[8], last_modified=row[9]
            )
            results.append(item)
        
        return results
    
    def get_related_items(self, item_id: str, relationship_type: str = None) -> List[IndexedItem]:
        """Get items related to a specific item"""
        cursor = self.db_connection.cursor()
        
        if relationship_type:
            query = """
                SELECT i.* FROM extP_index i
                JOIN relationships r ON i.id = r.to_item_id
                WHERE r.from_item_id = ? AND r.relationship_type = ?
            """
            params = [item_id, relationship_type]
        else:
            query = """
                SELECT i.* FROM extP_index i
                JOIN relationships r ON i.id = r.to_item_id
                WHERE r.from_item_id = ?
            """
            params = [item_id]
        
        cursor.execute(query, params)
        # Convert results to IndexedItem objects
        # ... (similar to query_index method)
        
        return []  # Simplified for brevity
    
    def check_for_changes(self) -> List[str]:
        """Check if any files have changed and need reindexing"""
        changed_files = []
        
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT DISTINCT source_file, hash FROM extP_index")
        indexed_files = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Check all files in ExtP directory
        for file_path in self.extP_path.rglob("*"):
            if file_path.is_file() and file_path.suffix in ['.py', '.json', '.md', '.txt']:
                rel_path = str(file_path.relative_to(self.extP_path))
                
                if rel_path in indexed_files:
                    # Check if file has changed
                    with open(file_path, 'r', encoding='utf-8') as f:
                        current_hash = self._calculate_hash(f.read())
                    
                    if current_hash != indexed_files[rel_path]:
                        changed_files.append(rel_path)
                else:
                    # New file
                    changed_files.append(rel_path)
        
        return changed_files
    
    def incremental_update(self) -> Dict[str, int]:
        """Update index for changed files only"""
        changed_files = self.check_for_changes()
        stats = {'updated': 0, 'added': 0, 'deleted': 0}
        
        for file_path in changed_files:
            full_path = self.extP_path / file_path
            if full_path.exists():
                # Remove old entries for this file
                cursor = self.db_connection.cursor()
                cursor.execute("DELETE FROM extP_index WHERE source_file = ?", (file_path,))
                
                # Re-index the file
                if full_path.suffix == '.py':
                    self._index_python_file(full_path, stats)
                elif full_path.suffix == '.json':
                    self._index_config_file(full_path, stats)
                elif full_path.suffix == '.md':
                    self._index_documentation_file(full_path, stats)
                
                stats['updated'] += 1
        
        self.db_connection.commit()
        return stats
    
    # Helper methods
    def _generate_id(self, item_type: str, file_path: Path, name: str, line: int) -> str:
        """Generate unique ID for an indexed item"""
        base = f"{item_type}:{file_path.name}:{name}:{line}"
        return hashlib.md5(base.encode()).hexdigest()
    
    def _calculate_hash(self, content: str) -> str:
        """Calculate hash of content for change detection"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity of a function"""
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
        return complexity
    
    def _get_decorator_name(self, decorator) -> str:
        """Get decorator name as string"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Attribute):
            return f"{decorator.attr}"
        else:
            return "unknown"
    
    def _get_base_name(self, base) -> str:
        """Get base class name as string"""
        if isinstance(base, ast.Name):
            return base.id
        else:
            return "unknown"
    
    def _flatten_config(self, config_data: dict, prefix: str = "") -> dict:
        """Flatten nested configuration data"""
        flattened = {}
        for key, value in config_data.items():
            full_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flattened.update(self._flatten_config(value, full_key))
            else:
                flattened[full_key] = value
        return flattened
    
    def _extract_requirements(self, content: str) -> Dict[str, str]:
        """Extract numbered requirements from markdown content"""
        requirements = {}
        # Look for patterns like "1.1.1", "2.3", etc.
        pattern = r'(\d+(?:\.\d+)*)\s+(.+?)(?=\n\d+\.\d+|\n#|\Z)'
        matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            req_id = match.group(1)
            req_text = match.group(2).strip()
            requirements[req_id] = req_text
        
        return requirements
    
    def _store_item(self, item: IndexedItem):
        """Store an indexed item in the database"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO extP_index 
            (id, type, name, source_file, line_number, content, context, metadata, hash, last_modified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item.id, item.type, item.name, item.source_file, item.line_number,
            item.content, item.context, json.dumps(item.metadata), item.hash, item.last_modified
        ))
    
    def _build_relationships(self):
        """Build relationships between indexed items"""
        # This would analyze imports, function calls, configuration usage, etc.
        # Simplified for brevity
        pass
    
    def _index_variable_assignment(self, node: ast.Assign, file_path: Path, content: str, stats: Dict[str, int]):
        """Index variable assignments that might be state variables"""
        # Look for potential state variables
        for target in node.targets:
            if isinstance(target, ast.Name):
                var_name = target.id
                if (var_name.isupper() or  # Constants
                    'state' in var_name.lower() or
                    'config' in var_name.lower() or
                    var_name.startswith('_')):  # Private variables
                    
                    lines = content.split('\n')
                    line_content = lines[node.lineno - 1] if node.lineno <= len(lines) else ""
                    
                    item = IndexedItem(
                        id=self._generate_id('state_var', file_path, var_name, node.lineno),
                        type='state_var',
                        name=var_name,
                        source_file=str(file_path.relative_to(self.extP_path)),
                        line_number=node.lineno,
                        content=line_content,
                        context=line_content,
                        metadata={'variable_type': 'assignment'},
                        hash=self._calculate_hash(line_content),
                        last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    )
                    
                    self._store_item(item)
                    stats['state_vars'] += 1
    
    def _index_text_file(self, file_path: Path, stats: Dict[str, int]):
        """Index text files (like simulation dictionaries)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Try to parse as JSON if it looks like JSON
            if content.strip().startswith('{'):
                try:
                    data = json.loads(content)
                    for key, value in data.items():
                        item = IndexedItem(
                            id=self._generate_id('simulation_rule', file_path, key, 0),
                            type='simulation_rule',
                            name=key,
                            source_file=str(file_path.relative_to(self.extP_path)),
                            line_number=0,
                            content=f"{key} -> {value}",
                            context=content[:200],
                            metadata={'trigger': key, 'action': value, 'file_type': 'simulation_dict'},
                            hash=self._calculate_hash(f"{key}{value}"),
                            last_modified=datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                        )
                        self._store_item(item)
                        stats['configs'] += 1
                except json.JSONDecodeError:
                    pass  # Not JSON, skip
                    
        except Exception as e:
            print(f"Error indexing text file {file_path}: {e}")

# Usage example
if __name__ == "__main__":
    indexer = ExtPIndexer("C:/Path/To/ExtP")
    
    # Build initial index
    stats = indexer.build_full_index()
    print(f"Initial indexing complete: {stats}")
    
    # Query examples
    functions = indexer.query_index(query_type='function', name_pattern='config')
    menus = indexer.query_index(query_type='menu')
    requirements = indexer.query_index(query_type='requirement')
    
    # Check for changes and update
    changes = indexer.check_for_changes()
    if changes:
        update_stats = indexer.incremental_update()
        print(f"Updated index: {update_stats}")
