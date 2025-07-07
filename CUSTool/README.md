# CUS - CLI User Simulator
## Intelligent Large-Scale CLI Testing Automation System

### Overview

The CLI User Simulator (CUS) has evolved into a comprehensive, intelligent testing automation system designed for large-scale CLI menu testing. The system now consists of multiple intelligent components that work together to automatically analyze, generate, and execute comprehensive test cases for any CLI application.

### Architecture

The system consists of four main components:

1. **CUS.py** - Core simulation engine with OCR-based CLI interaction
2. **TestCaseCreator.py** - Intelligent test case generation from source code analysis
3. **SequenceRunner.py** - Advanced test sequence execution manager
4. **MasterController.py** - Orchestrates the entire testing workflow

### Key Features

#### 🔍 **Intelligent Source Code Analysis**
- Automatically analyzes external program source code
- Extracts menu structures, options, and expected inputs
- Identifies navigation patterns and menu hierarchies
- Generates comprehensive simulation dictionaries

#### 🎯 **Smart Test Case Generation**
- Creates test sequences that cover all menu paths
- Generates edge case and stress test scenarios
- Prioritizes test cases based on importance and complexity
- Tracks coverage to ensure comprehensive testing

#### 🚀 **Advanced Test Execution**
- Executes test sequences with intelligent timing
- Manages state transitions and menu navigation
- Handles errors gracefully with retry logic
- Provides real-time monitoring and reporting

#### 📊 **Comprehensive Reporting**
- Generates detailed HTML and JSON reports
- Tracks coverage metrics and execution statistics
- Provides insights into untested menu paths
- Exports results for further analysis

### Quick Start

#### 1. Basic Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the Master Controller
python MasterController.py
```

#### 2. Full Automation Mode
```bash
# Run complete automation with default settings
python MasterController.py --auto
```

#### 3. Interactive Configuration
```bash
# Launch interactive mode for step-by-step configuration
python MasterController.py
```

### Detailed Usage

#### Configuration

Create a `master_config.json` file to configure the system:

```json
{
  "external_program": {
    "path": "C:\\path\\to\\your\\cli\\program.exe",
    "args": ["--arg1", "value1"],
    "working_directory": "C:\\path\\to\\working\\dir",
    "auto_launch": true,
    "auto_terminate": true
  },
  "source_analysis": {
    "enabled": true,
    "source_paths": [
      "C:\\path\\to\\source\\code\\folder",
      "C:\\path\\to\\specific\\file.py"
    ]
  },
  "test_execution": {
    "run_mode": "comprehensive",
    "priority_filter": [1, 2, 3],
    "retry_failures": true,
    "generate_reports": true
  }
}
```

#### Component Usage

##### TestCaseCreator - Standalone Analysis
```python
from TestCaseCreator import TestCaseCreator

# Create analyzer
creator = TestCaseCreator()

# Analyze source code
source_paths = ["C:\\path\\to\\source"]
results = creator.run_full_analysis(source_paths)

# Results include:
# - menu_options: Extracted menu structures
# - simulation_dict: Generated simulation dictionary
# - test_sequences: Intelligent test cases
# - coverage_report: Analysis of coverage gaps
```

##### SequenceRunner - Execute Tests
```python
from SequenceRunner import SequenceRunner

# Create runner
runner = SequenceRunner()

# Load test sequences
runner.load_test_sequences("test_sequences.json")

# Execute all sequences
runner.run_all_sequences()

# Generate reports
runner.generate_html_report()
runner.save_execution_log()
```

##### MasterController - Full Orchestration
```python
from MasterController import MasterController

# Create controller
controller = MasterController()

# Run full automation
controller.run_full_automation()

# Or use interactive mode
controller.interactive_mode()
```

### Advanced Features

#### 1. Intelligent Pattern Recognition
The system automatically recognizes common CLI patterns:
- Menu selection prompts
- Yes/No confirmations
- Password inputs
- Navigation commands
- Error handling sequences

#### 2. Adaptive Test Generation
- Analyzes code complexity to prioritize tests
- Generates edge cases based on input validation
- Creates stress tests for performance validation
- Handles nested menu structures intelligently

#### 3. Smart Execution Management
- Manages test sequence dependencies
- Handles dynamic menu changes
- Adapts timing based on system responsiveness
- Recovers from unexpected errors

#### 4. Comprehensive Coverage Tracking
- Tracks which menu paths have been tested
- Identifies untested code branches
- Measures test coverage percentage
- Suggests additional test cases for gaps

### File Structure

```
CUSTool/
├── CUS.py                      # Core simulation engine
├── TestCaseCreator.py          # Intelligent test generation
├── SequenceRunner.py           # Test execution manager
├── MasterController.py         # Main orchestrator
├── requirements.txt            # Dependencies
├── simulation_dictionary.txt   # Generated simulation rules
├── test_sequences.json         # Generated test sequences
├── master_config.json          # Main configuration
├── Results_YYYYMMDD_HHMMSS/    # Session results
│   ├── final_report.json       # Comprehensive report
│   ├── execution_report.html   # Visual report
│   ├── execution_log.json      # Detailed execution log
│   └── source_analysis.json    # Analysis results
└── Logs/                       # Legacy logs
    ├── CUSEvents/              # Simulation events
    └── Screenshots/            # Screen captures
```

### Workflow Examples

#### Example 1: Analyze New CLI Program
```bash
# 1. Configure the external program
python MasterController.py
# Choose option 1 to configure external program

# 2. Set source code paths
# Choose option 2 to configure source analysis

# 3. Run full analysis
# Choose option 9 for full automation
```

#### Example 2: Generate Tests for Existing Program
```python
# Direct API usage
from TestCaseCreator import TestCaseCreator

creator = TestCaseCreator()
results = creator.run_full_analysis([
    "C:\\MyProgram\\src\\menu.py",
    "C:\\MyProgram\\src\\cli.py"
])

print(f"Found {len(results['menu_options'])} menu options")
print(f"Generated {len(results['test_sequences'])} test sequences")
```

#### Example 3: Execute Specific Test Sequences
```python
from SequenceRunner import SequenceRunner

runner = SequenceRunner()
runner.load_test_sequences()

# Filter to high-priority tests only
runner.sequences = [seq for seq in runner.sequences if seq.priority == 1]

# Execute filtered sequences
runner.run_all_sequences()
```

### Integration with Existing CUS

The new components are designed to work seamlessly with the existing CUS.py:

1. **TestCaseCreator** generates simulation dictionaries that CUS.py can use
2. **SequenceRunner** can launch and coordinate with CUS.py for actual simulation
3. **MasterController** manages the entire pipeline including CUS coordination

### Configuration Options

#### TestCaseCreator Configuration
```json
{
  "menu_patterns": [
    "Select an option.*?:",
    "Please enter your choice.*?:",
    "Choose.*?:"
  ],
  "input_patterns": [
    "Enter (\\w+):",
    "\\((\\w+)\\/(\\w+)\\)"
  ],
  "common_inputs": {
    "menu_select": ["1", "2", "3", "4", "5"],
    "yes_no": ["y", "n", "yes", "no"],
    "password": ["password", "123456", "admin"]
  }
}
```

#### SequenceRunner Configuration
```json
{
  "execution_settings": {
    "step_timeout": 30,
    "sequence_timeout": 300,
    "retry_failed_steps": true,
    "max_retries": 3,
    "adaptive_timing": true
  },
  "monitoring": {
    "screenshot_on_error": true,
    "log_level": "INFO",
    "state_tracking": true
  }
}
```

### Reporting and Analysis

#### HTML Reports
- Visual representation of test execution
- Step-by-step results with screenshots
- Coverage metrics and statistics
- Failed test analysis

#### JSON Logs
- Detailed execution data
- Performance metrics
- Error tracking
- Coverage analysis

#### Coverage Analysis
- Menu path coverage percentage
- Untested code branches
- Edge case coverage
- Performance bottlenecks

### Performance Considerations

#### Large-Scale Testing
- Parallel execution capabilities
- Memory-efficient sequence management
- Optimized screen capture and OCR
- Intelligent test prioritization

#### Resource Management
- Automatic cleanup of temporary files
- Memory usage monitoring
- CPU usage optimization
- Disk space management

### Troubleshooting

#### Common Issues
1. **OCR not working**: Ensure Tesseract is installed and in PATH
2. **External program not launching**: Check path and permissions
3. **Test sequences failing**: Verify simulation dictionary accuracy
4. **Performance issues**: Adjust timing settings and reduce concurrent sequences

#### Debug Mode
```python
# Enable debug mode for detailed logging
controller = MasterController()
controller.config["monitoring"]["log_level"] = "DEBUG"
```

### Future Enhancements

#### Planned Features
- Machine learning-based pattern recognition
- Dynamic test case generation based on execution results
- Integration with CI/CD pipelines
- Cloud-based test execution
- Real-time collaboration features

#### Extensibility
The system is designed to be easily extended:
- Custom pattern recognition modules
- Additional output formats
- Integration with testing frameworks
- Custom execution strategies

### Contributing

To extend the system:

1. **Add new patterns**: Modify `testcase_config.json`
2. **Custom execution logic**: Extend `SequenceRunner` class
3. **New analysis methods**: Add to `TestCaseCreator`
4. **Additional reporting**: Extend reporting functions

### License

This project is part of the CUS CLI testing automation system.

---

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

**Remember**: This system is designed for comprehensive, intelligent CLI testing. Start with small test cases and gradually scale up to full automation for best results.
