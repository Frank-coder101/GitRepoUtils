# ExtP Requirements Analysis Workflow

## Overview
This workflow generates requirements validation rules for CUS (CLI User Simulator) using GitHub Copilot analysis of ExtP (External Program) systems.

## Files Generated
- `generate_extp_requirements.py` - Main generator script
- `extp_analysis_prompt_optimized.txt` - Standardized prompt for Copilot
- `prompt_metadata.json` - Context metadata for reference

## Step-by-Step Workflow

### 1. Generate Analysis Prompt
```bash
python generate_extp_requirements.py ExternalProjectTarget\DeFiHuddleTradingSystem --requirements-file ExternalProjectTarget\DeFiHuddleTradingSystem\docs\Project_Requirements.md --exclude-patterns tests/ UserSimulator/ __pycache__/ retrospectives/ --llm gpt-4-1106-preview
```

**Optional parameters:**
- `--requirements-file "path/to/requirements.md"` - Specific requirements document
- `--requirements-folder "path/to/requirements/"` - Folder with requirements docs
- `--output-metadata "metadata.json"` - Save context metadata

### 2. Copy Prompt to GitHub Copilot Chat
1. Open the generated `analysis_prompt.txt` file
2. Copy the entire content
3. Paste into GitHub Copilot Chat in VS Code
4. Wait for Copilot to generate the three JSON files

### 3. Save Generated JSON Files
Copilot will generate three files. Save them as:
- `requirements.json` - Application requirements and workflows
- `validation_rules.json` - Screen progression and error classification
- `test_scenarios.json` - Comprehensive test scenarios

### 4. Update CUS to Use Requirements
Modify CUS.py to load and validate against the generated requirements:

```python
# At startup
requirements = load_json("requirements.json")
validation_rules = load_json("validation_rules.json")
test_scenarios = load_json("test_scenarios.json")

# In main monitoring loop
def validate_screen_progression(current_screen, action, next_screen):
    expected = validation_rules["screen_progressions"].get(current_screen, {}).get(action)
    if expected and next_screen != expected["expected_to_screen"]:
        return "CRITICAL: Workflow progression failure"
    return "SUCCESS"
```

#### Implementation Note: Requirements-Driven Validation and Defect Prompt Integration

After integrating the requirements, validation rules, and test scenarios as described above, the CUS system now performs requirements-driven validation of workflow progression in the main monitoring loop. Specifically:

- After each simulated action, CUS compares the screen content before and after the action (using OCR) to determine the actual transition.
- The function `validate_screen_progression(current_screen, action, next_screen)` is called with the before/after screen content and the action performed. This checks the transition against the loaded validation rules.
- If a workflow progression failure is detected (i.e., the transition does not match the requirements), this is now included in the error context passed to the `IssuePromptGenerator`.
- The defect prompt generated for the failure (saved in `UserSimulator/DefectPrompts`) is augmented with details about the requirements-driven validation failure, including the expected and actual screens, the action, and the specific rule violated.
- No separate output is created for requirements validation failures; instead, the existing defect prompt/reporting system is made more accurate and requirements-aware.

This ensures that all workflow progression failures are traceable to requirements and validation rules, and that defect prompts provide actionable, requirements-driven feedback for remediation.

## Expected Output Structure

### requirements.json
- Application metadata and description
- Expected workflows with triggers and responses
- Screen definitions and available actions
- Critical requirements that must be validated

### validation_rules.json
- Screen progression rules (A + action → B)
- Error classification (CRITICAL/WARNING/INFO)
- Timeout settings for various operations
- Success/failure criteria for each progression

### test_scenarios.json
- Step-by-step test scenarios
- Priority levels (CRITICAL/HIGH/MEDIUM/LOW)
- Success and failure criteria
- Expected screen progressions

## Key Benefits

### Requirements-Driven Validation
- Validates against intended behavior, not just code behavior
- Distinguishes critical workflow failures from implementation details
- Ensures ExtP meets user requirements

### Screen-by-Screen Progression
- Defines expected state transitions
- Detects when ExtP gets stuck or loops incorrectly
- Validates that actions produce expected results

### Error Classification
- **CRITICAL**: Requirements violations, workflow failures
- **WARNING**: Code behavior mismatches, timing issues  
- **INFO**: Normal operations, successful fallbacks

## Troubleshooting

### Prompt Too Large
If the generated prompt exceeds safe limits:
1. Check file sizes in the ExtP directory
2. Move large files out of the main directory temporarily
3. Use `--requirements-file` instead of auto-discovery
4. Reduce the number of auto-discovered files

### Missing Context
If Copilot needs more context:
1. Add specific requirements files with `--requirements-file`
2. Ensure main.py and key CLI files are in the ExtP directory
3. Check that README.md contains workflow descriptions

### Generated JSON Issues
If Copilot generates incomplete JSON:
1. Ask Copilot to regenerate specific sections
2. Validate JSON syntax before saving
3. Add missing fields based on the expected structure

## Example Usage

```bash
# Basic analysis
python generate_extp_requirements.py "C:\Projects\MyExtP"

# With specific requirements
python generate_extp_requirements.py "C:\Projects\MyExtP" \
  --requirements-file "C:\Projects\MyExtP\docs\requirements.md" \
  --output-prompt "my_analysis.txt"

# With requirements folder
python generate_extp_requirements.py "C:\Projects\MyExtP" \
  --requirements-folder "C:\Projects\MyExtP\specifications" \
  --output-prompt "comprehensive_analysis.txt"
```

## Integration with CUS

Once you have the three JSON files:

1. **Place files in CUS directory** - Same folder as CUS.py
2. **Modify CUS startup** - Load requirements at initialization
3. **Enhance validation logic** - Check progressions against rules
4. **Update error reporting** - Use new classification system
5. **Run enhanced tests** - Validate requirements compliance

This workflow transforms CUS from a simple input simulator into a comprehensive requirements validation system.

# Comprehensive ExtP Analysis: Configuration & State Management

## 1. Configuration Mechanisms in ExtP

### Primary Configuration Sources

Based on the requirements document and implementation references, ExtP uses multiple configuration layers:

#### 1.1 Environment-Driven Configuration (Section 24.4)
```
EXECUTION_MODE environment variable determines all settings:
- backtest: Mock data sources, no external dependencies
- live: IBKR_HOST, IBKR_PORT, IBKR_CLIENT_ID required
- unit: Simulated environment 
- integration: All external integrations active
```

#### 1.2 User Configuration Interface (Section 4.1)
```
- Simple GUI/CLI configuration wizard
- Grouped settings (funds, trade settings, risk settings)
- Expandable/collapsible sections
- Contextual help and tooltips for each setting
- No manual config file editing required
```

#### 1.3 Runtime Configuration Files
```
Based on CUS integration patterns:
- master_config.json: Main orchestrator settings
- sequence_runner_config.json: Test execution parameters  
- simulation_dictionary.txt: Trigger-action mappings
- exploration_plan.json: Systematic test scenarios
```

### 1.4 Key Configurable Parameters (from Requirements)

#### Trading Parameters
```
- Total funds available for trading (Section 3.1.1.1)
- Minimum position size (configurable)
- Maximum position size (configurable) 
- Risk thresholds (Section 11.1.3)
- Trailing stop percentage (Section 11.6.3, default: 2%)
```

#### Time-Based Settings
```
- Shrink Down Time Offset (default: 15 minutes) (Section 7.1.1.4.1)
- Cutoff Time Offset (default: 5 minutes) (Section 7.1.1.4.2)
- Cycle timing intervals (Section 7.1.3)
- Market hours handling (Section 20.1)
```

#### Analysis Weights (Section 6.1)
```
- Technical analysis method weights (0-100 each):
  - Regression forecasting weight
  - Regime states weight  
  - Candle patterns weight (all 20 patterns)
  - SMA weights (5, 9, 55, 200)
  - EMA 21 weight
  - RSI/CMF/MACD weights
  - Multi-timeframe multiplier factors
```

#### Risk Management
```
- Minimum acceptable score (default: 60/100) (Section 11.2.1)
- Liquidation risk threshold (configurable) (Section 11.1.1)
- Trade halt risk threshold (default: 5%) (Section 11.1.2)
- Margin usage threshold (default: 80%) (Section 17.2)
```

## 2. State Variables and Runtime Data

### 2.1 Portfolio State
```
- Current positions with scores (`portfolio positions score` list)
- Available funds calculation
- Position sizing constraints
- Open orders tracking
```

### 2.2 Market Data State  
```
- Symbol price histories
- Real-time price feeds
- Exchange hours and time zones (Section 2.7)
- Market scanning results (`opportunities_identified` list)
```

### 2.3 Analysis State
```
- Technical indicator calculations
- Regime state classifications (Scalp, Long, Take Profit, Reversal, Liquidate, Short)
- Multi-timeframe analysis results
- Score calculations per analysis method
```

### 2.4 Execution Cycle State
```
- Cycle A (Portfolio Protection): Every minute
- Cycle B (Opportunity Monitoring): Every minute  
- Average cycle time tracking
- Preemption hierarchy management
```

### 2.5 Persistent State (Section 16.1)
```
Saved every 30 seconds (configurable):
- Portfolio positions and scores
- Current active orders  
- Execution cycle status and counters
- Watchlist symbols and status
```

## 3. Configuration Management Architecture

### 3.1 Layered Configuration System
```
1. Default values (hardcoded)
2. Configuration files (JSON)
3. Environment variables  
4. User interface overrides
5. Runtime adjustments
```

### 3.2 Configuration Validation
```
- Input validation with error messages (Section 4.6.1)
- Range checking for numeric values
- Dependency validation (e.g., live mode requirements)
- Backup and restore mechanisms (Section 5.3.4.3)
```

### 3.3 Dynamic Configuration Updates
```
- Auto-tuning capability (Section 5.3.2)
- Real-time parameter adjustment
- Configuration change logging
- Rollback to "last known good version" (Section 5.3.5.2)
```

## 4. State Persistence and Recovery

### 4.1 Crash Recovery (Section 16)
```
- State snapshots every 30 seconds
- Automatic detection of previous session
- User choice: resume or start clean
- Order reconciliation on restart
```

### 4.2 Audit and Logging (Section 3.1.5)
```
- Unified audit log with unique identifiers
- All orders, rejections, confirmations
- Profit/loss tracking
- Call stack references for exceptions
```

### 4.3 Training and Enhancement Logs (Section 5.3.1)
```
- Machine learning activity tracking
- Configuration change history
- Performance metrics over time
- Enhancement activation records
```

## 5. Integration Points with CUS

### 5.1 Configuration Discovery
```
CUS can extract configuration from:
- ExtP source code analysis
- Documentation parsing (requirements.md)
- Runtime configuration files
- Environment variable detection
```

### 5.2 State Monitoring  
```
CUS monitors for:
- Configuration prompts and menus
- State change confirmations
- Error conditions and recovery
- Mode transitions (backtest/live)
```

### 5.3 Validation Testing
```
CUS validates:
- Configuration completeness
- State persistence across restarts
- Error handling robustness
- User interface responsiveness
```

## 6. Practical Implementation Details

### 6.1 File Locations
```
Based on CUS integration patterns:
- Main config: ./config/main_config.json
- Trading params: ./config/trading_params.json  
- Risk settings: ./config/risk_management.json
- State backup: ./state/backup_YYYYMMDD_HHMMSS.json
```

### 6.2 Environment Setup
```
Required environment variables for live mode:
- EXECUTION_MODE=live
- IBKR_HOST=127.0.0.1 (or broker host)
- IBKR_PORT=7497 (or broker port)  
- IBKR_CLIENT_ID=1 (unique identifier)
```

### 6.3 Configuration Wizard Flow
```
1. Mode selection (backtest/live)
2. Funds configuration  
3. Risk tolerance settings
4. Broker connection (if live)
5. Analysis preferences
6. Validation and confirmation
```

This comprehensive analysis provides the foundation for CUS to effectively test and validate all aspects of ExtP's configuration and state management systems.
