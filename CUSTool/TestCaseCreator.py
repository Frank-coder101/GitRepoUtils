#!/usr/bin/env python3
"""
TestCaseCreator - Intelligent Test Case Generation for CLI User Simulator

This module analyzes external programs, extracts menu structures, and automatically
generates comprehensive test sequences for full CLI menu coverage.

Features:
- Source code analysis to extract menu options
- Behavioral pattern recognition
- Automatic simulation dictionary generation
- Intelligent test sequence creation
- Coverage tracking and gap analysis
"""

import os
import re
import json
import random
import time
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class MenuOption:
    """Represents a menu option with its context and expected inputs"""
    trigger: str
    expected_inputs: List[str]
    context: str
    menu_level: int
    parent_menu: Optional[str] = None
    leads_to: Optional[str] = None
    is_terminal: bool = False
    source_file: Optional[str] = None
    documentation_refs: List[str] = field(default_factory=list)

@dataclass
class TestSequence:
    """Represents a complete test sequence through menu hierarchy"""
    name: str
    description: str
    steps: List[Dict[str, str]]
    expected_path: List[str]
    coverage_tags: Set[str]
    priority: int = 1  # 1=high, 2=medium, 3=low

@dataclass
class DocumentationInsight:
    """Represents insights extracted from documentation"""
    source_file: str
    insight_type: str  # 'requirement', 'test_case', 'user_story', 'flow', 'error_condition'
    content: str
    related_menus: List[str] = field(default_factory=list)
    priority: int = 1
    test_suggestions: List[str] = field(default_factory=list)

class TestCaseCreator:
    """
    Analyzes external programs and creates comprehensive test cases
    """
    
    def __init__(self, config_file: str = "testcase_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.menu_options: Dict[str, MenuOption] = {}
        self.test_sequences: List[TestSequence] = []
        self.coverage_map: Dict[str, bool] = {}
        self.simulation_dict: Dict[str, str] = {}
        self.documentation_insights: List[DocumentationInsight] = []
        self.blueprint_paths: List[str] = []
        
    def _load_config(self) -> Dict:
        """Load configuration for test case creation"""
        default_config = {
            "source_paths": [],
            "blueprint_paths": [],  # New: Documentation and blueprint paths
            "menu_patterns": [
                r"Select an option.*?:",
                r"Please enter your choice.*?:",
                r"Choose.*?:",
                r"Enter.*?:",
                r"Continue.*?\?",
                r"Press.*?to.*?:",
                r"\[.*?\].*?:",
                r"\d+\.\s+.*"
            ],
            "input_patterns": [
                r"Enter (\w+):",
                r"Please enter (\w+):",
                r"Input (\w+):",
                r"\((\w+)\/(\w+)\)",
                r"\[(\w+)\]"
            ],
            "terminal_indicators": [
                "exit", "quit", "bye", "goodbye", "terminate", "end", "finish"
            ],
            "common_inputs": {
                "menu_select": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
                "yes_no": ["y", "n", "yes", "no"],
                "continue": ["enter", "space", "any"],
                "text_input": ["test", "sample", "default", "admin", "user"],
                "password": ["password", "123456", "admin", "test123"]
            },
            "sequence_priorities": {
                "main_menu": 1,
                "setup_wizard": 1,
                "configuration": 2,
                "advanced_options": 3,
                "debug_mode": 3
            },
            "documentation_analysis": {
                "enabled": True,
                "file_patterns": ["*.md", "*.txt", "*.rst", "*.doc", "*.docx"],
                "key_sections": [
                    "requirements", "test cases", "user stories", "flows", 
                    "menus", "navigation", "errors", "exceptions", "scenarios"
                ],
                "requirement_patterns": [
                    r"(?i)requirement\s*\d+",
                    r"(?i)user\s+story\s*\d+",
                    r"(?i)test\s+case\s*\d+",
                    r"(?i)scenario\s*\d+"
                ],
                "menu_flow_patterns": [
                    r"(?i)menu\s+flow",
                    r"(?i)navigation\s+path",
                    r"(?i)user\s+journey",
                    r"(?i)workflow"
                ]
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}, using defaults")
        
        return default_config
    
    def analyze_source_code(self, source_paths: List[str]) -> Dict[str, MenuOption]:
        """
        Analyze source code files to extract menu structures and options
        """
        print("=== ANALYZING SOURCE CODE ===")
        menu_options = {}
        
        for source_path in source_paths:
            if not os.path.exists(source_path):
                print(f"Warning: Source path {source_path} does not exist")
                continue
                
            print(f"Analyzing: {source_path}")
            
            if os.path.isfile(source_path):
                self._analyze_file(source_path, menu_options)
            elif os.path.isdir(source_path):
                self._analyze_directory(source_path, menu_options)
        
        self.menu_options = menu_options
        print(f"Extracted {len(menu_options)} menu options")
        return menu_options
    
    def _analyze_file(self, file_path: str, menu_options: Dict[str, MenuOption]):
        """Analyze a single file for menu patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Extract menu patterns
            for pattern in self.config["menu_patterns"]:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    trigger = match.group(0).strip()
                    context = self._extract_context(content, match.start(), match.end())
                    
                    # Determine expected inputs
                    expected_inputs = self._determine_expected_inputs(trigger, context)
                    
                    # Determine menu level and relationships
                    menu_level = self._determine_menu_level(context)
                    parent_menu = self._find_parent_menu(context)
                    
                    # Check if this is a terminal option
                    is_terminal = any(term in trigger.lower() for term in self.config["terminal_indicators"])
                    
                    menu_option = MenuOption(
                        trigger=trigger,
                        expected_inputs=expected_inputs,
                        context=context,
                        menu_level=menu_level,
                        parent_menu=parent_menu,
                        is_terminal=is_terminal,
                        source_file=file_path  # Track source file
                    )
                    
                    menu_options[trigger] = menu_option
                    
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
    
    def _analyze_directory(self, dir_path: str, menu_options: Dict[str, MenuOption]):
        """Recursively analyze directory for source files"""
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if file.endswith(('.py', '.cpp', '.c', '.java', '.cs', '.js', '.ts', '.go', '.rs')):
                    file_path = os.path.join(root, file)
                    self._analyze_file(file_path, menu_options)
    
    def _extract_context(self, content: str, start: int, end: int, window: int = 500) -> str:
        """Extract context around a match"""
        context_start = max(0, start - window)
        context_end = min(len(content), end + window)
        return content[context_start:context_end]
    
    def _determine_expected_inputs(self, trigger: str, context: str) -> List[str]:
        """Determine what inputs are expected for a given trigger"""
        expected_inputs = []
        
        # Check for specific input patterns
        for pattern in self.config["input_patterns"]:
            matches = re.finditer(pattern, context, re.IGNORECASE)
            for match in matches:
                expected_inputs.extend(match.groups())
        
        # If no specific patterns found, use common inputs based on trigger type
        if not expected_inputs:
            if any(keyword in trigger.lower() for keyword in ["select", "option", "choice", "menu"]):
                expected_inputs = self.config["common_inputs"]["menu_select"]
            elif any(keyword in trigger.lower() for keyword in ["yes", "no", "continue"]):
                expected_inputs = self.config["common_inputs"]["yes_no"]
            elif "password" in trigger.lower():
                expected_inputs = self.config["common_inputs"]["password"]
            elif "enter" in trigger.lower():
                expected_inputs = self.config["common_inputs"]["text_input"]
            else:
                expected_inputs = ["enter", "1", "y"]  # Default fallback
        
        return expected_inputs
    
    def _determine_menu_level(self, context: str) -> int:
        """Determine the menu level based on context"""
        # Count indentation or nesting indicators
        lines = context.split('\n')
        avg_indent = sum(len(line) - len(line.lstrip()) for line in lines if line.strip()) / max(len(lines), 1)
        
        # Convert indentation to menu level
        if avg_indent <= 2:
            return 1  # Top level
        elif avg_indent <= 6:
            return 2  # Second level
        else:
            return 3  # Deep level
    
    def _find_parent_menu(self, context: str) -> Optional[str]:
        """Find the parent menu based on context"""
        # Look for menu headers or previous menu options
        lines = context.split('\n')
        for line in lines:
            if "main menu" in line.lower() or "menu" in line.lower():
                return line.strip()
        return None
    
    def generate_simulation_dictionary(self) -> Dict[str, str]:
        """
        Generate a comprehensive simulation dictionary from analyzed menu options
        """
        print("=== GENERATING SIMULATION DICTIONARY ===")
        simulation_dict = {}
        
        for trigger, menu_option in self.menu_options.items():
            # Choose the most appropriate input for this trigger
            if menu_option.expected_inputs:
                # Use the first expected input as default
                action = f"type_{menu_option.expected_inputs[0]}"
            else:
                # Fallback to common actions
                if any(keyword in trigger.lower() for keyword in ["continue", "press", "any"]):
                    action = "press_enter"
                elif any(keyword in trigger.lower() for keyword in ["wait", "loading"]):
                    action = "wait_random"
                else:
                    action = "type_1"  # Default menu selection
            
            simulation_dict[trigger] = action
        
        # Add common variations and edge cases
        simulation_dict.update({
            "Press any key to continue": "press_enter",
            "Loading...": "wait_random",
            "Please wait...": "wait_random",
            "Error:": "press_enter",
            "Warning:": "type_y",
            "Are you sure?": "type_y",
            "Confirm?": "type_y"
        })
        
        self.simulation_dict = simulation_dict
        print(f"Generated {len(simulation_dict)} simulation rules")
        return simulation_dict
    
    def create_test_sequences(self) -> List[TestSequence]:
        """
        Create intelligent test sequences that cover all menu paths
        """
        print("=== CREATING TEST SEQUENCES ===")
        test_sequences = []
        
        # Create sequences for each menu level
        top_level_menus = [opt for opt in self.menu_options.values() if opt.menu_level == 1]
        
        for menu_option in top_level_menus:
            # Create comprehensive test sequence for this menu path
            sequence = self._create_sequence_for_menu(menu_option)
            if sequence:
                test_sequences.append(sequence)
        
        # Create edge case sequences
        edge_sequences = self._create_edge_case_sequences()
        test_sequences.extend(edge_sequences)
        
        # Create stress test sequences
        stress_sequences = self._create_stress_test_sequences()
        test_sequences.extend(stress_sequences)
        
        self.test_sequences = test_sequences
        print(f"Created {len(test_sequences)} test sequences")
        return test_sequences
    
    def _create_sequence_for_menu(self, menu_option: MenuOption) -> Optional[TestSequence]:
        """Create a test sequence for a specific menu option"""
        steps = []
        coverage_tags = set()
        
        # Add the main menu action
        steps.append({
            "trigger": menu_option.trigger,
            "action": f"type_{menu_option.expected_inputs[0]}" if menu_option.expected_inputs else "type_1",
            "description": f"Select menu option: {menu_option.trigger}"
        })
        
        coverage_tags.add(menu_option.trigger)
        
        # Add follow-up actions based on menu type
        if not menu_option.is_terminal:
            # Add navigation back to main menu
            steps.append({
                "trigger": "any",
                "action": "press_escape",
                "description": "Return to main menu"
            })
        
        # Determine priority
        priority = 1  # Default high priority
        for keyword, prio in self.config["sequence_priorities"].items():
            if keyword in menu_option.trigger.lower():
                priority = prio
                break
        
        sequence = TestSequence(
            name=f"test_{menu_option.trigger.replace(' ', '_').replace(':', '').lower()}",
            description=f"Test sequence for {menu_option.trigger}",
            steps=steps,
            expected_path=[menu_option.trigger],
            coverage_tags=coverage_tags,
            priority=priority
        )
        
        return sequence
    
    def _create_edge_case_sequences(self) -> List[TestSequence]:
        """Create sequences for edge cases and error conditions"""
        edge_sequences = []
        
        # Invalid input sequence
        edge_sequences.append(TestSequence(
            name="test_invalid_inputs",
            description="Test invalid menu inputs",
            steps=[
                {"trigger": "Select an option", "action": "type_999", "description": "Invalid menu option"},
                {"trigger": "Error:", "action": "press_enter", "description": "Acknowledge error"}
            ],
            expected_path=["Error handling"],
            coverage_tags={"error_handling", "invalid_input"},
            priority=2
        ))
        
        # Rapid input sequence
        edge_sequences.append(TestSequence(
            name="test_rapid_input",
            description="Test rapid key input",
            steps=[
                {"trigger": "any", "action": "type_1", "description": "Rapid input 1"},
                {"trigger": "any", "action": "type_2", "description": "Rapid input 2"},
                {"trigger": "any", "action": "type_3", "description": "Rapid input 3"}
            ],
            expected_path=["Rapid input handling"],
            coverage_tags={"stress_test", "rapid_input"},
            priority=3
        ))
        
        return edge_sequences
    
    def _create_stress_test_sequences(self) -> List[TestSequence]:
        """Create sequences for stress testing"""
        stress_sequences = []
        
        # Long running sequence
        stress_sequences.append(TestSequence(
            name="test_long_running",
            description="Long running menu navigation",
            steps=[
                {"trigger": "Select an option", "action": "type_1", "description": "Menu 1"},
                {"trigger": "Select an option", "action": "type_2", "description": "Menu 2"},
                {"trigger": "Select an option", "action": "type_3", "description": "Menu 3"},
                {"trigger": "Select an option", "action": "type_4", "description": "Menu 4"},
                {"trigger": "any", "action": "press_escape", "description": "Exit"}
            ],
            expected_path=["Long navigation"],
            coverage_tags={"stress_test", "long_running"},
            priority=3
        ))
        
        return stress_sequences
    
    def save_simulation_dictionary(self, filename: str = "simulation_dictionary.txt"):
        """Save the generated simulation dictionary to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.simulation_dict, f, indent=2)
            print(f"Simulation dictionary saved to {filename}")
        except Exception as e:
            print(f"Error saving simulation dictionary: {e}")
    
    def save_test_sequences(self, filename: str = "test_sequences.json"):
        """Save test sequences to file"""
        try:
            # Convert dataclasses to dictionaries for JSON serialization
            sequences_data = []
            for seq in self.test_sequences:
                seq_dict = {
                    "name": seq.name,
                    "description": seq.description,
                    "steps": seq.steps,
                    "expected_path": seq.expected_path,
                    "coverage_tags": list(seq.coverage_tags),
                    "priority": seq.priority
                }
                sequences_data.append(seq_dict)
            
            with open(filename, 'w') as f:
                json.dump(sequences_data, f, indent=2)
            print(f"Test sequences saved to {filename}")
        except Exception as e:
            print(f"Error saving test sequences: {e}")
    
    def generate_coverage_report(self) -> Dict[str, any]:
        """Generate a coverage report showing what has been tested"""
        report = {
            "total_menu_options": len(self.menu_options),
            "total_test_sequences": len(self.test_sequences),
            "coverage_by_level": {},
            "untested_options": [],
            "priority_distribution": {1: 0, 2: 0, 3: 0}
        }
        
        # Coverage by menu level
        for level in [1, 2, 3]:
            level_options = [opt for opt in self.menu_options.values() if opt.menu_level == level]
            report["coverage_by_level"][level] = len(level_options)
        
        # Priority distribution
        for seq in self.test_sequences:
            report["priority_distribution"][seq.priority] += 1
        
        # Find untested options
        tested_triggers = set()
        for seq in self.test_sequences:
            tested_triggers.update(seq.coverage_tags)
        
        for trigger in self.menu_options.keys():
            if trigger not in tested_triggers:
                report["untested_options"].append(trigger)
        
        return report
    
    def run_full_analysis(self, source_paths: List[str], blueprint_paths: List[str] = None) -> Dict[str, any]:
        """
        Run complete analysis and generate all test artifacts
        """
        print("=== STARTING FULL ANALYSIS ===")
        
        # Update config with provided source paths
        self.config["source_paths"] = source_paths
        if blueprint_paths:
            self.config["blueprint_paths"] = blueprint_paths
            self.blueprint_paths = blueprint_paths
        
        # Analyze source code
        menu_options = self.analyze_source_code(source_paths)
        
        # Analyze documentation if enabled and paths provided
        documentation_insights = []
        if self.config["documentation_analysis"]["enabled"] and blueprint_paths:
            documentation_insights = self.analyze_documentation(blueprint_paths)
        
        # Enhance menu options with documentation insights
        enhanced_menu_options = self._enhance_menu_options_with_docs(menu_options, documentation_insights)
        
        # Generate simulation dictionary (enhanced with documentation)
        simulation_dict = self.generate_simulation_dictionary()
        
        # Create test sequences (enhanced with documentation insights)
        test_sequences = self.create_enhanced_test_sequences() if documentation_insights else self.create_test_sequences()
        
        # Save artifacts
        self.save_simulation_dictionary()
        self.save_test_sequences()
        self.save_documentation_insights()
        
        # Generate coverage report
        coverage_report = self.generate_coverage_report()
        
        print("=== ANALYSIS COMPLETE ===")
        print(f"Menu options found: {len(menu_options)}")
        print(f"Documentation insights: {len(documentation_insights)}")
        print(f"Simulation rules generated: {len(simulation_dict)}")
        print(f"Test sequences created: {len(test_sequences)}")
        
        return {
            "menu_options": enhanced_menu_options,
            "documentation_insights": documentation_insights,
            "simulation_dict": simulation_dict,
            "test_sequences": test_sequences,
            "coverage_report": coverage_report
        }
    
    def analyze_documentation(self, blueprint_paths: List[str]) -> List[DocumentationInsight]:
        """
        Analyze documentation files to extract test requirements and insights
        """
        print("=== ANALYZING DOCUMENTATION AND BLUEPRINTS ===")
        insights = []
        
        for blueprint_path in blueprint_paths:
            if not os.path.exists(blueprint_path):
                print(f"Warning: Blueprint path {blueprint_path} does not exist")
                continue
                
            print(f"Analyzing documentation: {blueprint_path}")
            
            if os.path.isfile(blueprint_path):
                insight = self._analyze_document_file(blueprint_path)
                if insight:
                    insights.extend(insight)
            elif os.path.isdir(blueprint_path):
                insights.extend(self._analyze_document_directory(blueprint_path))
        
        self.documentation_insights = insights
        print(f"Extracted {len(insights)} documentation insights")
        return insights
    
    def _analyze_document_file(self, file_path: str) -> List[DocumentationInsight]:
        """Analyze a single documentation file"""
        insights = []
        
        try:
            # Check if file is a documentation file
            if not any(file_path.endswith(ext) for ext in ['.md', '.txt', '.rst']):
                return insights
            
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            filename = os.path.basename(file_path).lower()
            
            # Analyze different types of documentation
            if 'requirement' in filename:
                insights.extend(self._extract_requirements(file_path, content))
            elif 'test' in filename:
                insights.extend(self._extract_test_cases(file_path, content))
            elif 'architecture' in filename or 'design' in filename:
                insights.extend(self._extract_architecture_insights(file_path, content))
            elif 'flow' in filename or 'workflow' in filename:
                insights.extend(self._extract_flow_insights(file_path, content))
            else:
                # General analysis
                insights.extend(self._extract_general_insights(file_path, content))
                
        except Exception as e:
            print(f"Error analyzing document {file_path}: {e}")
        
        return insights
    
    def _analyze_document_directory(self, dir_path: str) -> List[DocumentationInsight]:
        """Recursively analyze documentation directory"""
        insights = []
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                if any(file.endswith(ext) for ext in ['.md', '.txt', '.rst']):
                    file_path = os.path.join(root, file)
                    insights.extend(self._analyze_document_file(file_path))
        
        return insights
    
    def _extract_requirements(self, file_path: str, content: str) -> List[DocumentationInsight]:
        """Extract requirements from requirements documents"""
        insights = []
        
        # Look for requirement patterns
        requirement_patterns = [
            r"(?i)(?:requirement|req)\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*(?:requirement|req)|\n\s*$|\n\s*\n)",
            r"(?i)(?:user story|story)\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*(?:user story|story)|\n\s*$|\n\s*\n)",
            r"(?i)(?:test case|tc)\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*(?:test case|tc)|\n\s*$|\n\s*\n)",
            r"(?i)(?:scenario)\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*(?:scenario)|\n\s*$|\n\s*\n)"
        ]
        
        for pattern in requirement_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                req_id = match.group(1)
                req_text = match.group(2).strip()
                
                # Extract related menus from requirement text
                related_menus = self._extract_menu_references(req_text)
                
                # Generate test suggestions
                test_suggestions = self._generate_test_suggestions_from_requirement(req_text)
                
                insight = DocumentationInsight(
                    source_file=file_path,
                    insight_type='requirement',
                    content=f"REQ {req_id}: {req_text}",
                    related_menus=related_menus,
                    priority=1,
                    test_suggestions=test_suggestions
                )
                insights.append(insight)
        
        return insights
    
    def _extract_test_cases(self, file_path: str, content: str) -> List[DocumentationInsight]:
        """Extract test cases from test documentation"""
        insights = []
        
        # Look for test case patterns
        test_patterns = [
            r"(?i)test\s+case\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*test\s+case|\n\s*$|\n\s*\n)",
            r"(?i)test\s+scenario\s*#?\s*(\d+):?\s*(.+?)(?=\n\s*test\s+scenario|\n\s*$|\n\s*\n)",
            r"(?i)should\s+(.+?)(?=\n\s*should|\n\s*$|\n\s*\n)"
        ]
        
        for pattern in test_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                if len(match.groups()) >= 2:
                    test_id = match.group(1)
                    test_text = match.group(2).strip()
                    content_text = f"TEST {test_id}: {test_text}"
                else:
                    test_text = match.group(1).strip()
                    content_text = f"TEST: {test_text}"
                
                related_menus = self._extract_menu_references(test_text)
                
                insight = DocumentationInsight(
                    source_file=file_path,
                    insight_type='test_case',
                    content=content_text,
                    related_menus=related_menus,
                    priority=1,
                    test_suggestions=[test_text]
                )
                insights.append(insight)
        
        return insights
    
    def _extract_architecture_insights(self, file_path: str, content: str) -> List[DocumentationInsight]:
        """Extract architecture and design insights"""
        insights = []
        
        # Look for menu flow descriptions
        flow_patterns = [
            r"(?i)menu\s+flow:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])",
            r"(?i)navigation:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])",
            r"(?i)user\s+journey:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])",
            r"(?i)workflow:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])"
        ]
        
        for pattern in flow_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                flow_text = match.group(1).strip()
                related_menus = self._extract_menu_references(flow_text)
                
                insight = DocumentationInsight(
                    source_file=file_path,
                    insight_type='flow',
                    content=flow_text,
                    related_menus=related_menus,
                    priority=2,
                    test_suggestions=self._generate_flow_test_suggestions(flow_text)
                )
                insights.append(insight)
        
        return insights
    
    def _extract_flow_insights(self, file_path: str, content: str) -> List[DocumentationInsight]:
        """Extract flow and workflow insights"""
        return self._extract_architecture_insights(file_path, content)
    
    def _extract_general_insights(self, file_path: str, content: str) -> List[DocumentationInsight]:
        """Extract general insights from any documentation"""
        insights = []
        
        # Look for error conditions
        error_patterns = [
            r"(?i)error\s+condition:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])",
            r"(?i)exception:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])",
            r"(?i)failure\s+case:?\s*(.+?)(?=\n\s*\n|\n\s*[A-Z])"
        ]
        
        for pattern in error_patterns:
            matches = re.finditer(pattern, content, re.MULTILINE | re.DOTALL)
            for match in matches:
                error_text = match.group(1).strip()
                
                insight = DocumentationInsight(
                    source_file=file_path,
                    insight_type='error_condition',
                    content=error_text,
                    related_menus=[],
                    priority=2,
                    test_suggestions=[f"Test error condition: {error_text}"]
                )
                insights.append(insight)
        
        return insights
    
    def _extract_menu_references(self, text: str) -> List[str]:
        """Extract menu references from text"""
        menu_refs = []
        
        # Look for menu-related keywords
        menu_patterns = [
            r"(?i)menu\s+(\w+)",
            r"(?i)option\s+(\w+)",
            r"(?i)select\s+(\w+)",
            r"(?i)choose\s+(\w+)",
            r"(?i)navigate\s+to\s+(\w+)"
        ]
        
        for pattern in menu_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                menu_refs.append(match.group(1))
        
        return list(set(menu_refs))  # Remove duplicates
    
    def _generate_test_suggestions_from_requirement(self, requirement_text: str) -> List[str]:
        """Generate test suggestions from requirement text"""
        suggestions = []
        
        # Generate suggestions based on requirement keywords
        if "login" in requirement_text.lower():
            suggestions.extend([
                "Test valid login credentials",
                "Test invalid login credentials",
                "Test empty login fields"
            ])
        elif "menu" in requirement_text.lower():
            suggestions.extend([
                "Test all menu options",
                "Test menu navigation",
                "Test menu validation"
            ])
        elif "input" in requirement_text.lower():
            suggestions.extend([
                "Test valid input",
                "Test invalid input",
                "Test empty input",
                "Test boundary conditions"
            ])
        else:
            suggestions.append(f"Test requirement: {requirement_text}")
        
        return suggestions
    
    def _generate_flow_test_suggestions(self, flow_text: str) -> List[str]:
        """Generate test suggestions from flow descriptions"""
        suggestions = []
        
        # Extract steps from flow
        steps = re.findall(r"(?i)(?:step\s+\d+|then|next|after):?\s*(.+?)(?=\n|$)", flow_text)
        
        for step in steps:
            suggestions.append(f"Test flow step: {step.strip()}")
        
        if not suggestions:
            suggestions.append(f"Test complete flow: {flow_text}")
        
        return suggestions

    def _enhance_menu_options_with_docs(self, menu_options: Dict[str, MenuOption], documentation_insights: List[DocumentationInsight]) -> Dict[str, MenuOption]:
        """
        Enhance menu options with documentation insights
        """
        print("=== ENHANCING MENU OPTIONS WITH DOCUMENTATION ===")
        
        enhanced_options = menu_options.copy()
        
        for insight in documentation_insights:
            # Find menu options that match the insight
            for menu_name, menu_option in enhanced_options.items():
                # Check if this insight relates to this menu option
                if self._is_insight_related_to_menu(insight, menu_option):
                    # Add documentation reference
                    menu_option.documentation_refs.append(insight.source_file)
                    
                    # Enhance expected inputs based on insight
                    if insight.insight_type == 'requirement':
                        additional_inputs = self._extract_inputs_from_requirement(insight.content)
                        menu_option.expected_inputs.extend(additional_inputs)
                        menu_option.expected_inputs = list(set(menu_option.expected_inputs))  # Remove duplicates
                    
                    print(f"Enhanced menu '{menu_name}' with insight from {os.path.basename(insight.source_file)}")
        
        return enhanced_options
    
    def _is_insight_related_to_menu(self, insight: DocumentationInsight, menu_option: MenuOption) -> bool:
        """
        Check if a documentation insight is related to a menu option
        """
        # Check if any related menus match
        for related_menu in insight.related_menus:
            if related_menu.lower() in menu_option.trigger.lower():
                return True
        
        # Check if insight content mentions menu trigger
        if menu_option.trigger.lower() in insight.content.lower():
            return True
        
        # Check for keyword matches
        menu_keywords = menu_option.trigger.lower().split()
        insight_keywords = insight.content.lower().split()
        
        common_keywords = set(menu_keywords) & set(insight_keywords)
        if len(common_keywords) > 0:
            return True
        
        return False
    
    def _extract_inputs_from_requirement(self, requirement_text: str) -> List[str]:
        """
        Extract expected inputs from requirement text
        """
        inputs = []
        
        # Look for specific input patterns in requirements
        input_patterns = [
            r"(?i)enter\s+(['\"]([^'\"]+)['\"])",
            r"(?i)input\s+(['\"]([^'\"]+)['\"])",
            r"(?i)type\s+(['\"]([^'\"]+)['\"])",
            r"(?i)select\s+(['\"]([^'\"]+)['\"])",
            r"(?i)choose\s+(['\"]([^'\"]+)['\"])"
        ]
        
        for pattern in input_patterns:
            matches = re.finditer(pattern, requirement_text)
            for match in matches:
                if len(match.groups()) >= 2:
                    inputs.append(match.group(2))
                else:
                    inputs.append(match.group(1))
        
        return inputs
    
    def save_documentation_insights(self, filename: str = "documentation_insights.json"):
        """Save documentation insights to file"""
        try:
            # Convert dataclasses to dictionaries for JSON serialization
            insights_data = []
            for insight in self.documentation_insights:
                insight_dict = {
                    "source_file": insight.source_file,
                    "insight_type": insight.insight_type,
                    "content": insight.content,
                    "related_menus": insight.related_menus,
                    "priority": insight.priority,
                    "test_suggestions": insight.test_suggestions
                }
                insights_data.append(insight_dict)
            
            with open(filename, 'w') as f:
                json.dump(insights_data, f, indent=2)
            print(f"Documentation insights saved to {filename}")
        except Exception as e:
            print(f"Error saving documentation insights: {e}")
    
    def create_enhanced_test_sequences(self) -> List[TestSequence]:
        """
        Create test sequences enhanced with documentation insights
        """
        print("=== CREATING ENHANCED TEST SEQUENCES ===")
        
        # Start with basic sequences
        test_sequences = self.create_test_sequences()
        
        # Add sequences based on documentation insights
        doc_sequences = []
        
        for insight in self.documentation_insights:
            if insight.insight_type == 'requirement':
                # Create test sequence for requirement
                seq = self._create_requirement_test_sequence(insight)
                if seq:
                    doc_sequences.append(seq)
            elif insight.insight_type == 'test_case':
                # Create test sequence for documented test case
                seq = self._create_documented_test_sequence(insight)
                if seq:
                    doc_sequences.append(seq)
            elif insight.insight_type == 'flow':
                # Create test sequence for documented flow
                seq = self._create_flow_test_sequence(insight)
                if seq:
                    doc_sequences.append(seq)
        
        # Combine sequences
        all_sequences = test_sequences + doc_sequences
        
        print(f"Created {len(doc_sequences)} additional sequences from documentation")
        return all_sequences
    
    def _create_requirement_test_sequence(self, insight: DocumentationInsight) -> Optional[TestSequence]:
        """Create a test sequence for a requirement"""
        steps = []
        
        # Extract steps from test suggestions
        for suggestion in insight.test_suggestions:
            step = {
                "trigger": "any",
                "action": "press_enter",
                "description": suggestion
            }
            steps.append(step)
        
        if not steps:
            return None
        
        sequence = TestSequence(
            name=f"req_test_{len(self.test_sequences)}",
            description=f"Test sequence for requirement: {insight.content[:50]}...",
            steps=steps,
            expected_path=[insight.content],
            coverage_tags=set([insight.insight_type, "requirement_based"]),
            priority=insight.priority
        )
        
        return sequence
    
    def _create_documented_test_sequence(self, insight: DocumentationInsight) -> Optional[TestSequence]:
        """Create a test sequence for a documented test case"""
        steps = []
        
        # Create steps based on the documented test case
        for suggestion in insight.test_suggestions:
            step = {
                "trigger": "any",
                "action": "press_enter",
                "description": suggestion
            }
            steps.append(step)
        
        if not steps:
            return None
        
        sequence = TestSequence(
            name=f"doc_test_{len(self.test_sequences)}",
            description=f"Documented test case: {insight.content[:50]}...",
            steps=steps,
            expected_path=[insight.content],
            coverage_tags=set([insight.insight_type, "documented_test"]),
            priority=insight.priority
        )
        
        return sequence
    
    def _create_flow_test_sequence(self, insight: DocumentationInsight) -> Optional[TestSequence]:
        """Create a test sequence for a documented flow"""
        steps = []
        
        # Create steps based on the documented flow
        for suggestion in insight.test_suggestions:
            step = {
                "trigger": "any",
                "action": "press_enter",
                "description": suggestion
            }
            steps.append(step)
        
        if not steps:
            return None
        
        sequence = TestSequence(
            name=f"flow_test_{len(self.test_sequences)}",
            description=f"Flow test: {insight.content[:50]}...",
            steps=steps,
            expected_path=[insight.content],
            coverage_tags=set([insight.insight_type, "flow_based"]),
            priority=insight.priority
        )
        
        return sequence

def main():
    """Main function for standalone execution"""
    print("=== TestCaseCreator Standalone Execution ===")
    
    # Example usage
    creator = TestCaseCreator()
    
    # Example source paths (you would provide actual paths)
    source_paths = [
        "C:\\path\\to\\external\\program\\source",
        "C:\\path\\to\\another\\source\\folder"
    ]
    
    print("Enter source paths to analyze (one per line, empty line to finish):")
    user_paths = []
    while True:
        path = input("Source path: ").strip()
        if not path:
            break
        if os.path.exists(path):
            user_paths.append(path)
        else:
            print(f"Path does not exist: {path}")
    
    if user_paths:
        source_paths = user_paths
    
    # Run analysis
    results = creator.run_full_analysis(source_paths)
    
    # Display results
    print("\n=== ANALYSIS RESULTS ===")
    print(f"Found {len(results['menu_options'])} menu options")
    print(f"Generated {len(results['simulation_dict'])} simulation rules")
    print(f"Created {len(results['test_sequences'])} test sequences")
    
    print("\n=== COVERAGE REPORT ===")
    coverage = results['coverage_report']
    print(f"Total menu options: {coverage['total_menu_options']}")
    print(f"Test sequences: {coverage['total_test_sequences']}")
    print(f"Untested options: {len(coverage['untested_options'])}")
    
    if coverage['untested_options']:
        print("Untested options:")
        for option in coverage['untested_options'][:5]:  # Show first 5
            print(f"  - {option}")
        if len(coverage['untested_options']) > 5:
            print(f"  ... and {len(coverage['untested_options']) - 5} more")

if __name__ == "__main__":
    main()
