"""
Auto-Generate Simulation Dictionary for CLI User Simulator (CUS)

This module analyzes ExtP's source code to automatically generate a comprehensive
simulation dictionary that covers all possible CLI menus, prompts, and options.
"""

import os
import re
import json
import time
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class MenuOption:
    """Represents a menu option found in source code"""
    prompt_text: str
    expected_inputs: List[str]
    source_file: str
    line_number: int
    context: str
    option_type: str  # 'menu', 'yes_no', 'input', 'password', 'number'
    
@dataclass
class SimulationRule:
    """Represents a simulation rule to be generated"""
    trigger: str
    action: str
    priority: int
    confidence: float
    source_context: str

class SourceCodeAnalyzer:
    """Analyzes source code to extract CLI prompts and menu options"""
    
    def __init__(self, source_path: str):
        self.source_path = Path(source_path)
        self.menu_options: List[MenuOption] = []
        self.simulation_rules: List[SimulationRule] = []
        
        # Common patterns for CLI prompts
        self.prompt_patterns = [
            # Menu selection patterns
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?(?:select|choose|option|menu).*?["\']',
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?\[\d+\].*?["\']',
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?\d+[\.\)]\s*.*?["\']',
            
            # Input prompts
            r'(?:input|scanf|cin|read|gets|getline)\s*\(?["\'].*?["\']',
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?(?:enter|input|type).*?["\']',
            
            # Yes/No prompts
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?\(y/n\).*?["\']',
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?(?:yes|no|y/n|Y/N).*?["\']',
            
            # Password prompts
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?(?:password|pass|pwd).*?["\']',
            
            # Continue/Press key prompts
            r'(?:print|printf|cout|echo|puts)\s*\(?["\'].*?(?:continue|press|key).*?["\']',
        ]
        
        # File extensions to analyze
        self.code_extensions = {'.py', '.cpp', '.c', '.java', '.js', '.cs', '.php', '.rb', '.go', '.rs'}
        
    def analyze_directory(self) -> List[MenuOption]:
        """Analyze all source files in the directory"""
        print(f"[Analyzer] Analyzing source code in: {self.source_path}")
        
        if not self.source_path.exists():
            print(f"[Analyzer] ERROR: Source path does not exist: {self.source_path}")
            return []
        
        total_files = 0
        analyzed_files = 0
        
        # Walk through all files
        for file_path in self.source_path.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.code_extensions:
                total_files += 1
                try:
                    self._analyze_file(file_path)
                    analyzed_files += 1
                except Exception as e:
                    print(f"[Analyzer] Error analyzing {file_path}: {e}")
        
        print(f"[Analyzer] Analyzed {analyzed_files}/{total_files} files")
        print(f"[Analyzer] Found {len(self.menu_options)} menu options")
        
        return self.menu_options
    
    def _analyze_file(self, file_path: Path):
        """Analyze a single source file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    self._analyze_line(line, str(file_path), line_num, content)
                    
        except Exception as e:
            print(f"[Analyzer] Error reading {file_path}: {e}")
    
    def _analyze_line(self, line: str, file_path: str, line_num: int, full_content: str):
        """Analyze a single line of code"""
        line = line.strip()
        if not line or line.startswith('//') or line.startswith('#'):
            return
        
        # Check each pattern
        for pattern in self.prompt_patterns:
            matches = re.finditer(pattern, line, re.IGNORECASE)
            for match in matches:
                self._extract_menu_option(match, line, file_path, line_num, full_content)
    
    def _extract_menu_option(self, match, line: str, file_path: str, line_num: int, full_content: str):
        """Extract menu option from matched pattern"""
        matched_text = match.group(0)
        
        # Extract the actual prompt text (remove quotes and function calls)
        prompt_text = self._clean_prompt_text(matched_text)
        if not prompt_text:
            return
        
        # Determine option type and expected inputs
        option_type, expected_inputs = self._determine_option_type(prompt_text, line, full_content)
        
        # Get context around the line
        context = self._get_context(full_content, line_num, 3)
        
        menu_option = MenuOption(
            prompt_text=prompt_text,
            expected_inputs=expected_inputs,
            source_file=file_path,
            line_number=line_num,
            context=context,
            option_type=option_type
        )
        
        self.menu_options.append(menu_option)
        print(f"[Analyzer] Found {option_type}: '{prompt_text}' in {os.path.basename(file_path)}:{line_num}")
    
    def _clean_prompt_text(self, matched_text: str) -> str:
        """Clean and extract the actual prompt text"""
        # Remove function calls and quotes
        text = re.sub(r'^.*?["\']', '', matched_text)
        text = re.sub(r'["\'].*?$', '', text)
        text = text.strip()
        
        # Remove common formatting
        text = re.sub(r'\\n', ' ', text)
        text = re.sub(r'\\t', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _determine_option_type(self, prompt_text: str, line: str, full_content: str) -> Tuple[str, List[str]]:
        """Determine the type of option and expected inputs"""
        prompt_lower = prompt_text.lower()
        
        # Yes/No questions
        if any(keyword in prompt_lower for keyword in ['(y/n)', 'yes/no', 'y/n']):
            return 'yes_no', ['y', 'n', 'yes', 'no']
        
        # Password prompts
        if any(keyword in prompt_lower for keyword in ['password', 'pass', 'pwd']):
            return 'password', ['password123', 'admin', 'test123']
        
        # Menu selections (numbered options)
        if re.search(r'\d+[\.\)]\s*\w+', prompt_text) or 'select' in prompt_lower or 'choose' in prompt_lower:
            # Try to extract menu numbers
            numbers = re.findall(r'(\d+)[\.\)]', prompt_text)
            if numbers:
                return 'menu', numbers
            else:
                # Default menu options
                return 'menu', ['1', '2', '3', '4', '5']
        
        # Continue/Press key prompts
        if any(keyword in prompt_lower for keyword in ['continue', 'press', 'key', 'enter']):
            return 'continue', ['']  # Just press Enter
        
        # Number input
        if any(keyword in prompt_lower for keyword in ['number', 'amount', 'quantity', 'count']):
            return 'number', ['1', '10', '100', '5']
        
        # Generic input
        return 'input', ['test', 'default', 'sample']
    
    def _get_context(self, content: str, line_num: int, context_lines: int) -> str:
        """Get context around a line"""
        lines = content.split('\n')
        start = max(0, line_num - context_lines - 1)
        end = min(len(lines), line_num + context_lines)
        
        context_lines_list = lines[start:end]
        return '\n'.join(context_lines_list)

class SimulationDictionaryGenerator:
    """Generates simulation dictionary from analyzed menu options"""
    
    def __init__(self, menu_options: List[MenuOption]):
        self.menu_options = menu_options
        self.simulation_rules: List[SimulationRule] = []
        
    def generate_rules(self) -> Dict[str, str]:
        """Generate simulation rules from menu options"""
        print(f"[Generator] Generating rules from {len(self.menu_options)} menu options")
        
        rules_dict = {}
        
        for option in self.menu_options:
            # Generate multiple rules for each option
            base_rules = self._generate_base_rules(option)
            
            for rule in base_rules:
                # Avoid duplicates
                if rule.trigger not in rules_dict:
                    rules_dict[rule.trigger] = rule.action
                    self.simulation_rules.append(rule)
        
        print(f"[Generator] Generated {len(rules_dict)} simulation rules")
        return rules_dict
    
    def _generate_base_rules(self, option: MenuOption) -> List[SimulationRule]:
        """Generate base rules for a menu option"""
        rules = []
        
        # Create variations of the prompt text
        variations = self._create_prompt_variations(option.prompt_text)
        
        for variation in variations:
            for expected_input in option.expected_inputs:
                action = self._determine_action(expected_input, option.option_type)
                
                rule = SimulationRule(
                    trigger=variation,
                    action=action,
                    priority=self._calculate_priority(option),
                    confidence=self._calculate_confidence(option),
                    source_context=f"{option.source_file}:{option.line_number}"
                )
                
                rules.append(rule)
        
        return rules
    
    def _create_prompt_variations(self, prompt_text: str) -> List[str]:
        """Create variations of prompt text for better matching"""
        variations = [prompt_text]
        
        # Add truncated versions
        if len(prompt_text) > 20:
            variations.append(prompt_text[:20] + "...")
            variations.append(prompt_text[-20:])
        
        # Add case variations
        variations.append(prompt_text.lower())
        variations.append(prompt_text.upper())
        
        # Add punctuation variations
        variations.append(prompt_text.rstrip('.:!?'))
        variations.append(prompt_text + ':')
        
        return list(set(variations))
    
    def _determine_action(self, expected_input: str, option_type: str) -> str:
        """Determine the action for an expected input"""
        if option_type == 'continue':
            return 'press_enter'
        elif option_type == 'password':
            return f'type_{expected_input}'
        elif expected_input == '':
            return 'press_enter'
        else:
            return f'type_{expected_input}'
    
    def _calculate_priority(self, option: MenuOption) -> int:
        """Calculate priority for a menu option"""
        # Higher priority for more specific prompts
        if option.option_type == 'menu':
            return 10
        elif option.option_type == 'yes_no':
            return 8
        elif option.option_type == 'password':
            return 9
        else:
            return 5
    
    def _calculate_confidence(self, option: MenuOption) -> float:
        """Calculate confidence score for a menu option"""
        # Higher confidence for clearer patterns
        confidence = 0.5
        
        if any(keyword in option.prompt_text.lower() for keyword in ['select', 'choose', 'option']):
            confidence += 0.3
        
        if re.search(r'\d+[\.\)]', option.prompt_text):
            confidence += 0.2
        
        return min(confidence, 1.0)

class SmartExplorer:
    """Intelligent exploration strategy for testing all CLI paths"""
    
    def __init__(self, simulation_rules: List[SimulationRule]):
        self.simulation_rules = simulation_rules
        self.coverage_tracker = CoverageTracker()
        self.exploration_strategy = "breadth_first"  # or "depth_first", "random"
    
    def generate_exploration_plan(self) -> List[Dict]:
        """Generate a plan for exploring all CLI paths"""
        print("[Explorer] Generating exploration plan...")
        
        # Group rules by menu type
        menu_rules = [r for r in self.simulation_rules if 'menu' in r.trigger.lower()]
        yes_no_rules = [r for r in self.simulation_rules if any(x in r.action for x in ['y', 'n'])]
        
        exploration_plan = []
        
        # Create test scenarios
        exploration_plan.extend(self._create_menu_exploration_scenarios(menu_rules))
        exploration_plan.extend(self._create_decision_tree_scenarios(yes_no_rules))
        
        print(f"[Explorer] Generated {len(exploration_plan)} exploration scenarios")
        return exploration_plan
    
    def _create_menu_exploration_scenarios(self, menu_rules: List[SimulationRule]) -> List[Dict]:
        """Create scenarios for exploring menu options"""
        scenarios = []
        
        for rule in menu_rules:
            scenario = {
                "name": f"Explore Menu: {rule.trigger}",
                "actions": [rule.action],
                "priority": rule.priority,
                "expected_prompts": [rule.trigger],
                "strategy": "systematic"
            }
            scenarios.append(scenario)
        
        return scenarios
    
    def _create_decision_tree_scenarios(self, yes_no_rules: List[SimulationRule]) -> List[Dict]:
        """Create scenarios for yes/no decision trees"""
        scenarios = []
        
        for rule in yes_no_rules:
            # Create both yes and no scenarios
            for choice in ['y', 'n']:
                scenario = {
                    "name": f"Decision: {rule.trigger} -> {choice}",
                    "actions": [f"type_{choice}"],
                    "priority": rule.priority,
                    "expected_prompts": [rule.trigger],
                    "strategy": "decision_tree"
                }
                scenarios.append(scenario)
        
        return scenarios

class CoverageTracker:
    """Tracks coverage of CLI paths during exploration"""
    
    def __init__(self):
        self.visited_prompts: Set[str] = set()
        self.visited_actions: Set[str] = set()
        self.path_coverage: Dict[str, int] = {}
        self.start_time = time.time()
    
    def track_interaction(self, prompt: str, action: str):
        """Track an interaction between CUS and ExtP"""
        self.visited_prompts.add(prompt)
        self.visited_actions.add(action)
        
        path_key = f"{prompt} -> {action}"
        self.path_coverage[path_key] = self.path_coverage.get(path_key, 0) + 1
    
    def get_coverage_report(self) -> Dict:
        """Get coverage report"""
        runtime = time.time() - self.start_time
        
        return {
            "runtime_seconds": runtime,
            "unique_prompts": len(self.visited_prompts),
            "unique_actions": len(self.visited_actions),
            "total_interactions": sum(self.path_coverage.values()),
            "path_coverage": dict(self.path_coverage),
            "visited_prompts": list(self.visited_prompts),
            "visited_actions": list(self.visited_actions)
        }

def main():
    """Main function to run the auto-generation process"""
    print("=== Auto-Generate Simulation Dictionary ===")
    
    # Configuration
    EXTP_SOURCE_PATH = input("Enter path to ExtP source code (or press Enter for default): ").strip()
    if not EXTP_SOURCE_PATH:
        EXTP_SOURCE_PATH = "C:\\Users\\gibea\\Documents\\ExtP"  # Default path
    
    OUTPUT_DICT_PATH = "simulation_dictionary_generated.json"
    EXPLORATION_PLAN_PATH = "exploration_plan.json"
    
    try:
        # Step 1: Analyze source code
        print(f"\nStep 1: Analyzing source code in {EXTP_SOURCE_PATH}")
        analyzer = SourceCodeAnalyzer(EXTP_SOURCE_PATH)
        menu_options = analyzer.analyze_directory()
        
        if not menu_options:
            print("No menu options found. Please check the source path.")
            return
        
        # Step 2: Generate simulation rules
        print(f"\nStep 2: Generating simulation rules...")
        generator = SimulationDictionaryGenerator(menu_options)
        rules_dict = generator.generate_rules()
        
        # Step 3: Create exploration plan
        print(f"\nStep 3: Creating exploration plan...")
        explorer = SmartExplorer(generator.simulation_rules)
        exploration_plan = explorer.generate_exploration_plan()
        
        # Step 4: Save results
        print(f"\nStep 4: Saving results...")
        
        # Save simulation dictionary
        with open(OUTPUT_DICT_PATH, 'w') as f:
            json.dump(rules_dict, f, indent=2)
        print(f"Simulation dictionary saved to: {OUTPUT_DICT_PATH}")
        
        # Save exploration plan
        with open(EXPLORATION_PLAN_PATH, 'w') as f:
            json.dump(exploration_plan, f, indent=2)
        print(f"Exploration plan saved to: {EXPLORATION_PLAN_PATH}")
        
        # Step 5: Generate summary report
        print(f"\n=== SUMMARY REPORT ===")
        print(f"Source files analyzed: {len(set(opt.source_file for opt in menu_options))}")
        print(f"Menu options found: {len(menu_options)}")
        print(f"Simulation rules generated: {len(rules_dict)}")
        print(f"Exploration scenarios: {len(exploration_plan)}")
        
        # Show some examples
        print(f"\nExample simulation rules:")
        for i, (trigger, action) in enumerate(list(rules_dict.items())[:5]):
            print(f"  {i+1}. '{trigger}' -> '{action}'")
        
        print(f"\nExample exploration scenarios:")
        for i, scenario in enumerate(exploration_plan[:3]):
            print(f"  {i+1}. {scenario['name']}")
        
        print(f"\nFiles created:")
        print(f"  - {OUTPUT_DICT_PATH}")
        print(f"  - {EXPLORATION_PLAN_PATH}")
        
    except Exception as e:
        print(f"Error during auto-generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
