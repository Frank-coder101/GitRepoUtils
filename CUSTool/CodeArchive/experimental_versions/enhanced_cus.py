"""
Enhanced CLI User Simulator (CUS) with Auto-Generated Dictionary Support

This enhanced version of CUS can:
1. Use auto-generated simulation dictionaries
2. Follow exploration plans for systematic testing
3. Track coverage of CLI paths
4. Generate comprehensive test reports
"""

import os
import time
import json
import random
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from pathlib import Path

# Import existing CUS components
import sys
sys.path.append('.')

# OCR and keyboard imports
try:
    from pynput.keyboard import Controller, Key
    import pyautogui
    import pytesseract
    from PIL import Image, ImageGrab
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    print("OCR libraries not available. Install pytesseract, pillow, and pynput.")

@dataclass
class TestScenario:
    """Represents a test scenario from the exploration plan"""
    name: str
    actions: List[str]
    priority: int
    expected_prompts: List[str]
    strategy: str
    completed: bool = False
    attempts: int = 0
    last_error: Optional[str] = None

class EnhancedCUS:
    """Enhanced CLI User Simulator with auto-generated dictionary support"""
    
    def __init__(self, config_path: str = "cus_config.json"):
        self.config = self._load_config(config_path)
        self.simulation_dictionary = {}
        self.exploration_plan: List[TestScenario] = []
        self.coverage_tracker = CoverageTracker()
        self.current_scenario_index = 0
        self.keyboard = Controller() if OCR_AVAILABLE else None
        
        # Paths
        self.simulation_dict_path = self.config.get('simulation_dictionary_path', 'simulation_dictionary_generated.json')
        self.exploration_plan_path = self.config.get('exploration_plan_path', 'exploration_plan.json')
        self.screenshots_path = self.config.get('screenshots_path', 'Logs/Screenshots')
        self.events_path = self.config.get('events_path', 'Logs/CUSEvents')
        self.reports_path = self.config.get('reports_path', 'Logs/Reports')
        
        # OCR Configuration
        self.screen_region = self.config.get('screen_region', None)
        self.poll_interval = self.config.get('poll_interval', 3)
        self.ocr_confidence_threshold = self.config.get('ocr_confidence_threshold', 0.7)
        
        # Create directories
        os.makedirs(self.screenshots_path, exist_ok=True)
        os.makedirs(self.events_path, exist_ok=True)
        os.makedirs(self.reports_path, exist_ok=True)
        
        print(f"[Enhanced CUS] Initialized with config: {config_path}")
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from file"""
        default_config = {
            "simulation_dictionary_path": "simulation_dictionary_generated.json",
            "exploration_plan_path": "exploration_plan.json",
            "screenshots_path": "Logs/Screenshots",
            "events_path": "Logs/CUSEvents",
            "reports_path": "Logs/Reports",
            "screen_region": None,
            "poll_interval": 3,
            "ocr_confidence_threshold": 0.7,
            "safe_mode": False,
            "exploration_mode": "systematic",  # or "random", "priority"
            "max_attempts_per_scenario": 3,
            "scenario_timeout": 60
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                custom_config = json.load(f)
                default_config.update(custom_config)
        
        return default_config
    
    def load_simulation_dictionary(self) -> bool:
        """Load simulation dictionary"""
        if os.path.exists(self.simulation_dict_path):
            with open(self.simulation_dict_path, 'r') as f:
                self.simulation_dictionary = json.load(f)
            print(f"[Enhanced CUS] Loaded {len(self.simulation_dictionary)} simulation rules")
            return True
        else:
            print(f"[Enhanced CUS] Simulation dictionary not found: {self.simulation_dict_path}")
            return False
    
    def load_exploration_plan(self) -> bool:
        """Load exploration plan"""
        if os.path.exists(self.exploration_plan_path):
            with open(self.exploration_plan_path, 'r') as f:
                plan_data = json.load(f)
                self.exploration_plan = [
                    TestScenario(**scenario) for scenario in plan_data
                ]
            print(f"[Enhanced CUS] Loaded {len(self.exploration_plan)} test scenarios")
            return True
        else:
            print(f"[Enhanced CUS] Exploration plan not found: {self.exploration_plan_path}")
            return False
    
    def capture_screen(self) -> tuple:
        """Capture screen with enhanced error handling"""
        try:
            if self.screen_region:
                screenshot = ImageGrab.grab(bbox=self.screen_region)
            else:
                screenshot = ImageGrab.grab()
            
            # Save screenshot with timestamp
            timestamp = int(time.time())
            screenshot_path = os.path.join(self.screenshots_path, f"screenshot_{timestamp}.png")
            screenshot.save(screenshot_path)
            
            return screenshot, screenshot_path
        except Exception as e:
            print(f"[Enhanced CUS] Error capturing screen: {e}")
            return None, None
    
    def extract_text_from_image(self, image) -> str:
        """Extract text from image using OCR"""
        try:
            text = pytesseract.image_to_string(image)
            return text.strip()
        except Exception as e:
            print(f"[Enhanced CUS] Error extracting text: {e}")
            return ""
    
    def find_best_match(self, screen_text: str) -> Optional[str]:
        """Find best matching trigger from simulation dictionary"""
        if not screen_text:
            return None
        
        screen_text_lower = screen_text.lower()
        best_match = None
        best_score = 0
        
        for trigger in self.simulation_dictionary.keys():
            trigger_lower = trigger.lower()
            
            # Exact match
            if trigger_lower in screen_text_lower:
                score = len(trigger_lower) / len(screen_text_lower)
                if score > best_score:
                    best_score = score
                    best_match = trigger
        
        return best_match if best_score > 0.3 else None
    
    def execute_action(self, action: str) -> bool:
        """Execute a simulation action"""
        if self.config.get('safe_mode', False):
            print(f"[Enhanced CUS] SAFE MODE: Would execute action '{action}'")
            return True
        
        try:
            if action.startswith('type_'):
                text = action[5:]  # Remove 'type_' prefix
                if text:
                    for char in text:
                        self.keyboard.type(char)
                        time.sleep(0.05)  # Small delay between characters
                
                # Press Enter after typing
                time.sleep(0.1)
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                
                print(f"[Enhanced CUS] Typed: '{text}' and pressed Enter")
                
            elif action == 'press_enter':
                self.keyboard.press(Key.enter)
                self.keyboard.release(Key.enter)
                print(f"[Enhanced CUS] Pressed Enter")
                
            elif action.startswith('wait_'):
                wait_time = int(action[5:]) if action[5:].isdigit() else 2
                time.sleep(wait_time)
                print(f"[Enhanced CUS] Waited {wait_time} seconds")
                
            else:
                print(f"[Enhanced CUS] Unknown action: {action}")
                return False
            
            return True
            
        except Exception as e:
            print(f"[Enhanced CUS] Error executing action '{action}': {e}")
            return False
    
    def log_event(self, event_type: str, details: Dict):
        """Log an event with detailed information"""
        timestamp = int(time.time())
        event_data = {
            "timestamp": timestamp,
            "event_type": event_type,
            "details": details
        }
        
        event_file = os.path.join(self.events_path, f"event_{timestamp}.json")
        with open(event_file, 'w') as f:
            json.dump(event_data, f, indent=2)
    
    def run_systematic_exploration(self):
        """Run systematic exploration of all scenarios"""
        print("[Enhanced CUS] Starting systematic exploration...")
        
        total_scenarios = len(self.exploration_plan)
        completed_scenarios = 0
        
        for i, scenario in enumerate(self.exploration_plan):
            print(f"\n[Enhanced CUS] Running scenario {i+1}/{total_scenarios}: {scenario.name}")
            
            success = self.run_scenario(scenario)
            if success:
                completed_scenarios += 1
                scenario.completed = True
                print(f"[Enhanced CUS] ✓ Scenario completed successfully")
            else:
                print(f"[Enhanced CUS] ✗ Scenario failed after {scenario.attempts} attempts")
        
        print(f"\n[Enhanced CUS] Exploration complete: {completed_scenarios}/{total_scenarios} scenarios completed")
    
    def run_scenario(self, scenario: TestScenario) -> bool:
        """Run a single test scenario"""
        scenario.attempts += 1
        start_time = time.time()
        
        try:
            # Wait for expected prompts
            for expected_prompt in scenario.expected_prompts:
                if not self.wait_for_prompt(expected_prompt, timeout=self.config.get('scenario_timeout', 60)):
                    scenario.last_error = f"Timeout waiting for prompt: {expected_prompt}"
                    return False
            
            # Execute actions
            for action in scenario.actions:
                if not self.execute_action(action):
                    scenario.last_error = f"Failed to execute action: {action}"
                    return False
                
                # Wait between actions
                time.sleep(1)
            
            # Log successful scenario
            self.log_event("scenario_completed", {
                "scenario_name": scenario.name,
                "actions": scenario.actions,
                "duration": time.time() - start_time,
                "attempts": scenario.attempts
            })
            
            return True
            
        except Exception as e:
            scenario.last_error = str(e)
            return False
    
    def wait_for_prompt(self, expected_prompt: str, timeout: int = 30) -> bool:
        """Wait for a specific prompt to appear"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            screenshot, screenshot_path = self.capture_screen()
            if screenshot:
                screen_text = self.extract_text_from_image(screenshot)
                
                if expected_prompt.lower() in screen_text.lower():
                    print(f"[Enhanced CUS] Found expected prompt: {expected_prompt}")
                    return True
            
            time.sleep(self.poll_interval)
        
        print(f"[Enhanced CUS] Timeout waiting for prompt: {expected_prompt}")
        return False
    
    def run_interactive_mode(self):
        """Run interactive mode with standard OCR monitoring"""
        print("[Enhanced CUS] Starting interactive mode...")
        
        loop_count = 0
        previous_text = ""
        
        while True:
            time.sleep(self.poll_interval)
            loop_count += 1
            
            # Capture and analyze screen
            screenshot, screenshot_path = self.capture_screen()
            if screenshot:
                current_text = self.extract_text_from_image(screenshot)
                
                if current_text != previous_text:
                    print(f"[Enhanced CUS] Screen changed, analyzing...")
                    
                    # Find matching trigger
                    trigger = self.find_best_match(current_text)
                    if trigger:
                        action = self.simulation_dictionary[trigger]
                        print(f"[Enhanced CUS] Found trigger: '{trigger}' -> '{action}'")
                        
                        # Execute action
                        if self.execute_action(action):
                            # Track coverage
                            self.coverage_tracker.track_interaction(trigger, action)
                            
                            # Log event
                            self.log_event("interaction", {
                                "trigger": trigger,
                                "action": action,
                                "screen_text": current_text,
                                "screenshot_path": screenshot_path
                            })
                        
                        time.sleep(2)  # Wait after action
                
                previous_text = current_text
            
            if loop_count % 10 == 0:
                print(f"[Enhanced CUS] Running... (loop {loop_count})")
    
    def generate_coverage_report(self):
        """Generate comprehensive coverage report"""
        coverage_data = self.coverage_tracker.get_coverage_report()
        
        # Add scenario completion data
        total_scenarios = len(self.exploration_plan)
        completed_scenarios = sum(1 for s in self.exploration_plan if s.completed)
        
        report = {
            "timestamp": int(time.time()),
            "coverage_summary": {
                "total_scenarios": total_scenarios,
                "completed_scenarios": completed_scenarios,
                "completion_rate": completed_scenarios / total_scenarios if total_scenarios > 0 else 0,
                "unique_prompts_found": coverage_data["unique_prompts"],
                "unique_actions_executed": coverage_data["unique_actions"],
                "total_interactions": coverage_data["total_interactions"],
                "runtime_minutes": coverage_data["runtime_seconds"] / 60
            },
            "detailed_coverage": coverage_data,
            "scenario_results": [
                {
                    "name": s.name,
                    "completed": s.completed,
                    "attempts": s.attempts,
                    "last_error": s.last_error
                }
                for s in self.exploration_plan
            ]
        }
        
        # Save report
        report_path = os.path.join(self.reports_path, f"coverage_report_{int(time.time())}.json")
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[Enhanced CUS] Coverage report saved to: {report_path}")
        return report

class CoverageTracker:
    """Enhanced coverage tracker"""
    
    def __init__(self):
        self.visited_prompts: Set[str] = set()
        self.visited_actions: Set[str] = set()
        self.interaction_log: List[Dict] = []
        self.start_time = time.time()
    
    def track_interaction(self, prompt: str, action: str):
        """Track an interaction"""
        self.visited_prompts.add(prompt)
        self.visited_actions.add(action)
        
        interaction = {
            "timestamp": time.time(),
            "prompt": prompt,
            "action": action
        }
        self.interaction_log.append(interaction)
    
    def get_coverage_report(self) -> Dict:
        """Get detailed coverage report"""
        return {
            "runtime_seconds": time.time() - self.start_time,
            "unique_prompts": len(self.visited_prompts),
            "unique_actions": len(self.visited_actions),
            "total_interactions": len(self.interaction_log),
            "interaction_log": self.interaction_log,
            "visited_prompts": list(self.visited_prompts),
            "visited_actions": list(self.visited_actions)
        }

def main():
    """Main function"""
    if not OCR_AVAILABLE:
        print("OCR libraries not available. Please install required packages.")
        return
    
    print("=== Enhanced CLI User Simulator ===")
    
    # Initialize Enhanced CUS
    cus = EnhancedCUS()
    
    # Load simulation dictionary and exploration plan
    if not cus.load_simulation_dictionary():
        print("Failed to load simulation dictionary. Run auto_generate_dictionary.py first.")
        return
    
    if not cus.load_exploration_plan():
        print("Failed to load exploration plan. Run auto_generate_dictionary.py first.")
        return
    
    # Choose mode
    mode = input("\nChoose mode:\n1. Interactive (standard OCR monitoring)\n2. Systematic (run all scenarios)\n3. Generate report only\nEnter choice (1-3): ").strip()
    
    try:
        if mode == "1":
            cus.run_interactive_mode()
        elif mode == "2":
            cus.run_systematic_exploration()
        elif mode == "3":
            pass  # Just generate report
        else:
            print("Invalid choice. Using interactive mode.")
            cus.run_interactive_mode()
    
    except KeyboardInterrupt:
        print("\n[Enhanced CUS] Interrupted by user")
    
    finally:
        # Generate final coverage report
        print("\n[Enhanced CUS] Generating coverage report...")
        report = cus.generate_coverage_report()
        
        # Print summary
        summary = report["coverage_summary"]
        print(f"\n=== FINAL SUMMARY ===")
        print(f"Scenarios completed: {summary['completed_scenarios']}/{summary['total_scenarios']} ({summary['completion_rate']:.1%})")
        print(f"Unique prompts found: {summary['unique_prompts_found']}")
        print(f"Unique actions executed: {summary['unique_actions_executed']}")
        print(f"Total interactions: {summary['total_interactions']}")
        print(f"Runtime: {summary['runtime_minutes']:.1f} minutes")

if __name__ == "__main__":
    main()
