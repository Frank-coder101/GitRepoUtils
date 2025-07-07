# Enhanced CLI User Simulator (CUS)

## Overview

The Enhanced CLI User Simulator (CUS) is a comprehensive automation system designed to simulate user interactions with command-line interfaces. It features auto-generation of simulation dictionaries, systematic exploration of all CLI paths, and intelligent testing strategies.

## 🚀 Key Features

### Auto-Generation System
- **Source Code Analysis**: Automatically scans ExtP's source code to find all CLI prompts and menu options
- **Intelligent Dictionary Generation**: Creates comprehensive simulation dictionaries with multiple response strategies
- **Exploration Planning**: Generates systematic test scenarios to cover all possible CLI paths
- **Smart Pattern Recognition**: Identifies menu selections, yes/no prompts, password inputs, and more

### Enhanced Simulation Engine
- **OCR-Based Monitoring**: Uses screen capture and OCR for real-time prompt detection
- **Intelligent Action Execution**: Simulates realistic keyboard input with proper timing
- **Coverage Tracking**: Monitors which prompts and actions have been tested
- **Error Handling**: Robust error recovery and logging systems

### Comprehensive Testing
- **Interactive Mode**: Real-time response to CLI prompts as they appear
- **Systematic Mode**: Methodical execution of all test scenarios
- **Coverage Analysis**: Detailed reports on test coverage and completion rates
- **Performance Metrics**: Runtime analysis and efficiency tracking

## 📁 Project Structure

```
CUSTool/
├── auto_generate_dictionary.py    # Auto-generates simulation dictionaries
├── enhanced_cus.py                # Enhanced CUS with full features
├── cus_config.json               # Configuration file
├── test_enhanced_cus.py          # Comprehensive test suite
├── run_enhanced_cus.bat          # Interactive batch menu
├── requirements_enhanced.txt      # All required packages
├── CUS.py                        # Original CUS implementation
├── simulation_dictionary.txt      # Manual simulation rules
├── Logs/                         # All log files and reports
│   ├── Screenshots/              # Screen captures for OCR
│   ├── CUSEvents/               # Simulation event logs
│   ├── Reports/                 # Coverage and performance reports
│   └── CUSErrors/               # Error logs
└── .vscode/
    └── tasks.json               # VS Code tasks for easy execution
```

## 🔧 Installation

### Prerequisites
1. **Python 3.7+** with pip
2. **Tesseract OCR** - Download from [UB-Mannheim](https://github.com/UB-Mannheim/tesseract/wiki)
3. **ExtP** - The external program you want to test

### Quick Setup
```bash
# Install required packages
pip install -r requirements_enhanced.txt

# Install Tesseract OCR (Windows)
winget install UB-Mannheim.TesseractOCR

# Test installation
python test_enhanced_cus.py
```

## 🎯 Usage

### Method 1: Interactive Batch Menu (Recommended)
```bash
# Run the interactive menu
run_enhanced_cus.bat
```

### Method 2: Direct Python Execution
```bash
# 1. Generate simulation dictionary
python auto_generate_dictionary.py

# 2. Run enhanced CUS
python enhanced_cus.py
```

### Method 3: VS Code Tasks
1. Open the project in VS Code
2. Press `Ctrl+Shift+P`
3. Type "Tasks: Run Task"
4. Select from available CUS tasks

## 🔄 Workflow

### Phase 1: Auto-Generation
1. **Analyze ExtP Source**: Point the analyzer to ExtP's source code directory
2. **Extract Prompts**: Automatically find all CLI prompts, menus, and input requests
3. **Generate Dictionary**: Create comprehensive simulation rules for all found prompts
4. **Create Exploration Plan**: Generate systematic test scenarios

### Phase 2: Testing
1. **Launch ExtP**: Start your external program
2. **Run CUS**: Choose interactive or systematic mode
3. **Monitor Progress**: Watch real-time coverage and interaction logs
4. **Review Results**: Analyze coverage reports and performance metrics

### Phase 3: Analysis
1. **Coverage Reports**: Detailed analysis of tested paths
2. **Performance Metrics**: Runtime and efficiency statistics
3. **Error Analysis**: Review any failures or issues
4. **Optimization**: Refine simulation rules based on results

## 📊 Configuration

### Basic Configuration (`cus_config.json`)
```json
{
  "safe_mode": false,
  "poll_interval": 3,
  "exploration_mode": "systematic",
  "max_attempts_per_scenario": 3,
  "scenario_timeout": 60
}
```

### Advanced OCR Settings
```json
{
  "ocr_preprocessing": {
    "resize_factor": 2,
    "convert_to_grayscale": true,
    "apply_threshold": true
  },
  "tesseract_config": "--psm 6 -c tessedit_char_whitelist=..."
}
```

## 🧪 Testing Modes

### 1. Interactive Mode
- Monitors screen continuously
- Responds to prompts as they appear
- Best for real-time testing and debugging

### 2. Systematic Mode
- Executes all planned test scenarios
- Methodical coverage of all CLI paths
- Best for comprehensive testing

### 3. Coverage Analysis Mode
- Generates reports without running tests
- Analyzes previous test results
- Best for performance analysis

## 📈 Reports and Analytics

### Coverage Reports
- **Prompt Coverage**: Which prompts were encountered
- **Action Coverage**: Which actions were executed
- **Path Coverage**: Which CLI paths were explored
- **Completion Rate**: Percentage of successful scenarios

### Performance Metrics
- **Runtime Analysis**: How long each scenario took
- **Error Rates**: Success/failure statistics
- **Efficiency Metrics**: Actions per minute, response times

### Error Analysis
- **Failed Scenarios**: Which tests failed and why
- **OCR Issues**: Text recognition problems
- **Timeout Analysis**: Scenarios that took too long

## 🔍 Advanced Features

### Intelligent Exploration
- **Priority-Based Testing**: High-priority scenarios first
- **Adaptive Strategies**: Different approaches for different prompt types
- **Context-Aware Responses**: Responses based on current CLI state

### OCR Optimization
- **Region-Based Capture**: Focus on specific screen areas
- **Preprocessing**: Image enhancement for better text recognition
- **Confidence Thresholds**: Quality control for text extraction

### Extensibility
- **Plugin System**: Add custom analyzers and generators
- **Custom Actions**: Define new simulation actions
- **Integration APIs**: Connect with external tools

## 🚨 Troubleshooting

### Common Issues

1. **Tesseract not found**
   - Install Tesseract OCR
   - Add to system PATH
   - Test with: `tesseract --version`

2. **OCR text not recognized**
   - Check screen resolution
   - Adjust OCR preprocessing settings
   - Verify console window visibility

3. **ExtP not responding**
   - Ensure ExtP is running
   - Check window focus
   - Verify prompt text matches dictionary

4. **Python package errors**
   - Update pip: `pip install --upgrade pip`
   - Install packages: `pip install -r requirements_enhanced.txt`
   - Check Python version: `python --version`

### Debug Mode
```bash
# Run with detailed logging
python enhanced_cus.py --debug

# Test individual components
python test_enhanced_cus.py
```

## 🤝 Contributing

### Adding New Features
1. Create new analyzer patterns in `auto_generate_dictionary.py`
2. Add new action types in `enhanced_cus.py`
3. Update configuration schema in `cus_config.json`
4. Add tests in `test_enhanced_cus.py`

### Improving OCR
1. Experiment with preprocessing options
2. Test different Tesseract configurations
3. Add custom text cleaning functions
4. Optimize for specific CLI interfaces

## 📝 License

This project is licensed under the MIT License. See LICENSE file for details.

## 🙏 Acknowledgments

- **Tesseract OCR** for text recognition
- **pynput** for keyboard simulation
- **PIL/Pillow** for image processing
- **pyautogui** for screen capture

---

## Quick Start Checklist

- [ ] Install Python 3.7+
- [ ] Install Tesseract OCR
- [ ] Run `pip install -r requirements_enhanced.txt`
- [ ] Test with `python test_enhanced_cus.py`
- [ ] Configure ExtP source path
- [ ] Run `run_enhanced_cus.bat`
- [ ] Choose option 1 to auto-generate dictionary
- [ ] Start ExtP
- [ ] Choose option 2 or 3 to run CUS
- [ ] Review coverage reports

For detailed documentation and examples, see the individual Python files and their docstrings.
