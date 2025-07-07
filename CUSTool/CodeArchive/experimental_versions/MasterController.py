#!/usr/bin/env python3
"""
CUS Master Controller - Intelligent CLI Testing Automation

This is the main controller that coordinates TestCaseCreator and SequenceRunner
to provide complete end-to-end automated CLI testing capabilities.

Features:
- Orchestrates the entire testing workflow
- Manages communication between components
- Provides unified interface for large-scale testing
- Handles configuration and reporting
- Manages external program lifecycle
- Integrates AI-optimized defect reporting system
"""

import os
import sys
import json
import time
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Import our components
from TestCaseCreator import TestCaseCreator
from SequenceRunner import SequenceRunner

# Import defect reporting
try:
    from IssuePromptGenerator import IssuePromptGenerator
    DEFECT_REPORTING_AVAILABLE = True
except ImportError:
    DEFECT_REPORTING_AVAILABLE = False
    print("Warning: Defect reporting not available - IssuePromptGenerator not found")

class MasterController:
    """
    Main controller for orchestrating intelligent CLI testing
    """
    
    def __init__(self, config_file: str = "master_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.test_creator = None
        self.sequence_runner = None
        self.external_process = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results_dir = f"Results_{self.session_id}"
        
        # Defect reporting status
        self.defect_reporting_enabled = (
            DEFECT_REPORTING_AVAILABLE and 
            self.config.get("defect_reporting", {}).get("enabled", False)
        )
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        print(f"Session: {self.session_id}")
        print(f"Results directory: {self.results_dir}")
        
        if self.defect_reporting_enabled:
            print("✓ Defect reporting system enabled")
        else:
            print("✗ Defect reporting system disabled")
    
    def _load_config(self) -> Dict:
        """Load master configuration"""
        default_config = {
            "external_program": {
                "path": "",
                "args": [],
                "working_directory": "",
                "launch_delay": 5,
                "auto_launch": True,
                "auto_terminate": True
            },
            "source_analysis": {
                "enabled": True,
                "source_paths": [],
                "blueprint_paths": [],  # New: Documentation and blueprint paths
                "patterns": {
                    "menu_indicators": ["menu", "option", "choice", "select"],
                    "input_indicators": ["enter", "input", "type", "password"],
                    "exit_indicators": ["exit", "quit", "bye", "terminate"]
                }
            },
            "test_execution": {
                "run_mode": "comprehensive",  # comprehensive, quick, custom
                "max_execution_time": 3600,  # 1 hour
                "priority_filter": [1, 2, 3],  # Which priorities to run
                "retry_failures": True,
                "generate_reports": True
            },
            "integration": {
                "use_existing_cus": True,
                "cus_script": "CUS.py",
                "monitor_external_errors": True,
                "adaptive_timing": True
            },
            "reporting": {
                "generate_html": True,
                "generate_json": True,
                "save_screenshots": True,
                "detailed_logs": True
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
    
    def initialize_components(self) -> bool:
        """Initialize TestCaseCreator and SequenceRunner"""
        try:
            print("=== INITIALIZING COMPONENTS ===")
            
            # Initialize TestCaseCreator
            print("Initializing TestCaseCreator...")
            self.test_creator = TestCaseCreator()
            
            # Initialize SequenceRunner
            print("Initializing SequenceRunner...")
            self.sequence_runner = SequenceRunner()
            
            print("Components initialized successfully")
            return True
            
        except Exception as e:
            print(f"Error initializing components: {e}")
            return False
    
    def launch_external_program(self) -> bool:
        """Launch the external program to be tested"""
        if not self.config["external_program"]["auto_launch"]:
            print("Auto-launch disabled. Please start the external program manually.")
            return True
        
        try:
            print("=== LAUNCHING EXTERNAL PROGRAM ===")
            
            program_path = self.config["external_program"]["path"]
            if not program_path:
                print("No external program path specified in config")
                return False
            
            if not os.path.exists(program_path):
                print(f"External program not found: {program_path}")
                return False
            
            # Build command
            cmd = [program_path] + self.config["external_program"]["args"]
            working_dir = self.config["external_program"]["working_directory"] or os.path.dirname(program_path)
            
            print(f"Command: {' '.join(cmd)}")
            print(f"Working directory: {working_dir}")
            
            # Launch process
            self.external_process = subprocess.Popen(
                cmd,
                cwd=working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait for program to start
            delay = self.config["external_program"]["launch_delay"]
            print(f"Waiting {delay} seconds for program to start...")
            time.sleep(delay)
            
            # Check if process is still running
            if self.external_process.poll() is None:
                print("External program launched successfully")
                return True
            else:
                print("External program terminated unexpectedly")
                return False
                
        except Exception as e:
            print(f"Error launching external program: {e}")
            return False
    
    def analyze_and_generate_tests(self) -> bool:
        """Analyze source code and generate test cases"""
        if not self.config["source_analysis"]["enabled"]:
            print("Source analysis disabled, skipping test generation")
            return True
        
        try:
            print("=== ANALYZING SOURCE CODE ===")
            
            source_paths = self.config["source_analysis"]["source_paths"]
            blueprint_paths = self.config["source_analysis"]["blueprint_paths"]
            
            if not source_paths:
                print("No source paths specified, using interactive mode")
                source_paths = self._get_source_paths_interactive()
            
            if not blueprint_paths:
                print("No blueprint paths specified, using interactive mode")
                blueprint_paths = self._get_blueprint_paths_interactive()
            
            if not source_paths:
                print("No source paths provided, skipping analysis")
                return False
            
            # Run analysis
            results = self.test_creator.run_full_analysis(source_paths, blueprint_paths)
            
            # Save results to session directory
            analysis_file = os.path.join(self.results_dir, "source_analysis.json")
            with open(analysis_file, 'w') as f:
                json.dump({
                    "timestamp": datetime.now().isoformat(),
                    "source_paths": source_paths,
                    "menu_options_found": len(results["menu_options"]),
                    "simulation_rules_generated": len(results["simulation_dict"]),
                    "test_sequences_created": len(results["test_sequences"]),
                    "coverage_report": results["coverage_report"]
                }, f, indent=2)
            
            print(f"Analysis complete. Results saved to: {analysis_file}")
            return True
            
        except Exception as e:
            print(f"Error during analysis: {e}")
            return False
    
    def _get_source_paths_interactive(self) -> List[str]:
        """Get source paths interactively from user"""
        print("Enter source paths to analyze (one per line, empty line to finish):")
        paths = []
        while True:
            path = input("Source path: ").strip()
            if not path:
                break
            if os.path.exists(path):
                paths.append(path)
                print(f"Added: {path}")
            else:
                print(f"Path does not exist: {path}")
        return paths
    
    def _get_blueprint_paths_interactive(self) -> List[str]:
        """Get blueprint/documentation paths interactively from user"""
        print("Enter blueprint/documentation paths to analyze (one per line, empty line to finish):")
        print("Examples: ./docs, ./requirements, ./blueprints")
        paths = []
        while True:
            path = input("Blueprint path: ").strip()
            if not path:
                break
            if os.path.exists(path):
                paths.append(path)
                print(f"Added: {path}")
            else:
                print(f"Path does not exist: {path}")
        return paths
    
    def execute_test_sequences(self) -> bool:
        """Execute all test sequences"""
        try:
            print("=== EXECUTING TEST SEQUENCES ===")
            
            # Load test sequences
            if not self.sequence_runner.load_test_sequences():
                print("Failed to load test sequences")
                return False
            
            # Filter sequences based on configuration
            self._filter_sequences()
            
            # Execute sequences
            success = self.sequence_runner.run_all_sequences()
            
            # Save execution results
            log_file = os.path.join(self.results_dir, "execution_log.json")
            self.sequence_runner.save_execution_log(log_file)
            
            if self.config["reporting"]["generate_html"]:
                html_file = os.path.join(self.results_dir, "execution_report.html")
                self.sequence_runner.generate_html_report(html_file)
            
            return success
            
        except Exception as e:
            print(f"Error executing test sequences: {e}")
            return False
    
    def _filter_sequences(self):
        """Filter sequences based on configuration"""
        if not self.sequence_runner.sequences:
            return
        
        # Filter by priority
        priority_filter = self.config["test_execution"]["priority_filter"]
        if priority_filter:
            filtered_sequences = [
                seq for seq in self.sequence_runner.sequences
                if seq.priority in priority_filter
            ]
            self.sequence_runner.sequences = filtered_sequences
            print(f"Filtered to {len(filtered_sequences)} sequences based on priority")
        
        # Filter by run mode
        run_mode = self.config["test_execution"]["run_mode"]
        if run_mode == "quick":
            # Only run priority 1 sequences
            quick_sequences = [seq for seq in self.sequence_runner.sequences if seq.priority == 1]
            self.sequence_runner.sequences = quick_sequences
            print(f"Quick mode: running {len(quick_sequences)} high-priority sequences")
    
    def monitor_execution(self) -> Dict:
        """Monitor the execution progress"""
        if not self.sequence_runner:
            return {"status": "not_initialized"}
        
        status = self.sequence_runner.get_execution_status()
        
        # Add external program status
        if self.external_process:
            status["external_program_running"] = self.external_process.poll() is None
        
        return status
    
    def terminate_external_program(self):
        """Terminate the external program"""
        if self.external_process and self.config["external_program"]["auto_terminate"]:
            try:
                print("Terminating external program...")
                self.external_process.terminate()
                
                # Wait for graceful termination
                try:
                    self.external_process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    print("Force killing external program...")
                    self.external_process.kill()
                
                print("External program terminated")
                
            except Exception as e:
                print(f"Error terminating external program: {e}")
    
    def generate_final_report(self) -> str:
        """Generate final comprehensive report"""
        try:
            print("=== GENERATING FINAL REPORT ===")
            
            report_file = os.path.join(self.results_dir, "final_report.json")
            
            # Collect all data
            report_data = {
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat(),
                "configuration": self.config,
                "external_program": {
                    "launched": self.external_process is not None,
                    "running": self.external_process.poll() is None if self.external_process else False
                },
                "analysis_performed": self.test_creator is not None,
                "execution_performed": self.sequence_runner is not None,
                "results_directory": self.results_dir
            }
            
            # Add execution metrics if available
            if self.sequence_runner:
                report_data["execution_metrics"] = {
                    "total_sequences": self.sequence_runner.metrics.total_sequences,
                    "completed_sequences": self.sequence_runner.metrics.completed_sequences,
                    "failed_sequences": self.sequence_runner.metrics.failed_sequences,
                    "total_execution_time": self.sequence_runner.metrics.total_execution_time,
                    "coverage_percentage": self.sequence_runner.metrics.coverage_percentage
                }
            
            # Save report
            with open(report_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            
            print(f"Final report saved: {report_file}")
            return report_file
            
        except Exception as e:
            print(f"Error generating final report: {e}")
            return ""
    
    def run_full_automation(self) -> bool:
        """Run complete end-to-end automation"""
        try:
            print("=== STARTING FULL AUTOMATION ===")
            print(f"Session: {self.session_id}")
            
            # Step 1: Initialize components
            if not self.initialize_components():
                print("Failed to initialize components")
                return False
            
            # Step 2: Launch external program
            if not self.launch_external_program():
                print("Failed to launch external program")
                return False
            
            # Step 3: Analyze and generate tests
            if not self.analyze_and_generate_tests():
                print("Failed to analyze and generate tests")
                return False
            
            # Step 4: Execute test sequences
            if not self.execute_test_sequences():
                print("Test execution completed with errors")
                # Continue to generate report even if tests failed
            
            # Step 5: Generate final report
            report_file = self.generate_final_report()
            
            print("=== AUTOMATION COMPLETED ===")
            print(f"Results available in: {self.results_dir}")
            if report_file:
                print(f"Final report: {report_file}")
            
            return True
            
        except Exception as e:
            print(f"Error during full automation: {e}")
            return False
        finally:
            # Always try to terminate external program
            self.terminate_external_program()
    
    def interactive_mode(self):
        """Run in interactive mode"""
        print("=== CUS MASTER CONTROLLER - INTERACTIVE MODE ===")
        
        while True:
            print("\n=== MAIN MENU ===")
            print("1. Configure external program")
            print("2. Configure source analysis")
            print("3. Initialize components")
            print("4. Launch external program")
            print("5. Analyze source code")
            print("6. Execute test sequences")
            print("7. Monitor execution")
            print("8. Generate reports")
            print("9. Run full automation")
            print("10. Save configuration")
            print("11. Exit")
            
            choice = input("Enter your choice (1-11): ").strip()
            
            if choice == "1":
                self._configure_external_program()
            elif choice == "2":
                self._configure_source_analysis()
            elif choice == "3":
                self.initialize_components()
            elif choice == "4":
                self.launch_external_program()
            elif choice == "5":
                self.analyze_and_generate_tests()
            elif choice == "6":
                self.execute_test_sequences()
            elif choice == "7":
                status = self.monitor_execution()
                print("\n=== EXECUTION STATUS ===")
                for key, value in status.items():
                    print(f"{key}: {value}")
            elif choice == "8":
                self.generate_final_report()
            elif choice == "9":
                self.run_full_automation()
            elif choice == "10":
                self._save_configuration()
            elif choice == "11":
                print("Exiting...")
                self.terminate_external_program()
                break
            else:
                print("Invalid choice. Please try again.")
    
    def _configure_external_program(self):
        """Configure external program settings"""
        print("\n=== CONFIGURE EXTERNAL PROGRAM ===")
        
        current_path = self.config["external_program"]["path"]
        path = input(f"Program path [{current_path}]: ").strip()
        if path:
            self.config["external_program"]["path"] = path
        
        args = input(f"Program arguments [{' '.join(self.config['external_program']['args'])}]: ").strip()
        if args:
            self.config["external_program"]["args"] = args.split()
        
        auto_launch = input(f"Auto-launch? [{'yes' if self.config['external_program']['auto_launch'] else 'no'}]: ").strip().lower()
        if auto_launch in ['yes', 'y']:
            self.config["external_program"]["auto_launch"] = True
        elif auto_launch in ['no', 'n']:
            self.config["external_program"]["auto_launch"] = False
        
        print("External program configuration updated")
    
    def _configure_source_analysis(self):
        """Configure source analysis settings"""
        print("\n=== CONFIGURE SOURCE ANALYSIS ===")
        
        enabled = input(f"Enable source analysis? [{'yes' if self.config['source_analysis']['enabled'] else 'no'}]: ").strip().lower()
        if enabled in ['yes', 'y']:
            self.config["source_analysis"]["enabled"] = True
        elif enabled in ['no', 'n']:
            self.config["source_analysis"]["enabled"] = False
        
        if self.config["source_analysis"]["enabled"]:
            print("Enter source paths (one per line, empty line to finish):")
            paths = []
            while True:
                path = input("Source path: ").strip()
                if not path:
                    break
                if os.path.exists(path):
                    paths.append(path)
                    print(f"Added: {path}")
                else:
                    print(f"Path does not exist: {path}")
            
            if paths:
                self.config["source_analysis"]["source_paths"] = paths
        
        print("Source analysis configuration updated")
    
    def _save_configuration(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving configuration: {e}")

def main():
    """Main entry point"""
    print("=== CUS MASTER CONTROLLER ===")
    print("Intelligent CLI Testing Automation System")
    print()
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--auto":
            # Run in full automation mode
            controller = MasterController()
            controller.run_full_automation()
        elif sys.argv[1] == "--help":
            print("Usage:")
            print("  python MasterController.py                 # Interactive mode")
            print("  python MasterController.py --auto          # Full automation mode")
            print("  python MasterController.py --config FILE   # Use specific config file")
            print("  python MasterController.py --help          # Show this help")
        elif sys.argv[1] == "--config" and len(sys.argv) > 2:
            # Use specific config file
            controller = MasterController(sys.argv[2])
            controller.interactive_mode()
        else:
            print(f"Unknown argument: {sys.argv[1]}")
            print("Use --help for usage information")
    else:
        # Run in interactive mode
        controller = MasterController()
        controller.interactive_mode()

if __name__ == "__main__":
    main()
