# CUS-ExtP Input Simulation Testing Guide

## ⚠️ IMPORTANT: Single Terminal Workflow

**MEMORIZED WORKFLOW - MUST FOLLOW:**
1. **Kill all terminals** (close any existing terminal windows)
2. **AI Assistant launches a new terminal in the CUSTool directory** (not GitRepoUtils)
3. **AI Assistant runs all commands in that single terminal** - never open another terminal
4. **AI Assistant navigates to CUSTool directory:** `cd C:\Users\gibea\Documents\GitRepoUtils\CUSTool`
5. **All testing must be done by the AI Assistant in this single terminal**

**WHO RUNS WHAT:**
- **AI Assistant responsibility:** Launch terminal, navigate directories, run all Python commands
- **User responsibility:** Provide instructions and monitor results and always launches the external program (ExtP)
- **NEVER:** User should not run commands manually unless explicitly requested

This workflow ensures proper environment isolation and prevents conflicts between multiple terminal sessions. The AI Assistant should execute all commands using the run_in_terminal tool.

## Quick Start - Manual Testing

**EXECUTION RESPONSIBILITY:** All commands below should be executed by the AI Assistant using the run_in_terminal tool, NOT by the user manually.

### Method 1: Basic Test (Recommended - AI Assistant Executes)
```bash
# AI Assistant runs the quick test script
.\test_cus_extp_quick.bat
```

### Method 2: Manual Step-by-Step (AI Assistant Execution)
1. **AI Assistant navigates to CUSTool directory:**
   ```bash
   cd C:\Users\gibea\Documents\GitRepoUtils\CUSTool
   ```

2. **AI Assistant launches ExtP first:**
   ```bash
   .\\_ExtPStartupManual.bat
   ```

3. **Wait for ExtP menu** (look for "Select an option:")

4. **AI Assistant launches CUS in the same terminal:**
   ```bash
   python CUS.py
   ```

5. **Observe the interaction:**
   - CUS should detect ExtP prompts
   - CUS should send keyboard inputs (like "1")
   - ExtP should respond to the inputs

### Method 3: Enhanced CUS Test (AI Assistant Execution)
```bash
# AI Assistant runs: Test with false negative detection
python EnhancedCUS.py
```

## What to Look For

### ✅ Successful Input Simulation
- CUS detects "Select an option:" prompt
- CUS sends "1" key press
- ExtP responds with next menu or action
- No legitimate error messages in CUS logs
- False positives from OCR misreading are automatically filtered out

### 🚨 False Negative Detection
- ExtP shows "Trading system is already configured"
- CUS detects this as false negative (95% confidence)
- CUS applies remediation (tries alternative actions)
- Configuration interface eventually appears

### 📊 Monitoring Points
- **CUS Logs**: Check `Logs/` folder for CUS events
- **Error Events**: Check `NewErrors/` for any issues
- **Screen Changes**: Watch for CUS responding to screen content
- **Keyboard Simulation**: Verify CUS is sending key presses

## Test Scenarios to Validate

### Scenario 1: Menu Navigation
- **Trigger**: "Select an option:"
- **Expected Input**: "1"
- **Expected Result**: ExtP advances to next menu

### Scenario 2: Configuration Request
- **Trigger**: "Configure trading system"
- **Expected Input**: Menu selection
- **Expected Result**: Configuration interface appears

### Scenario 3: False Negative Handling
- **Trigger**: "Trading system is already configured"
- **Expected Input**: Remediation actions
- **Expected Result**: Configuration forced or alternative path

## Automated Testing Options

### Option 1: Integration Test Suite
```bash
python test_cus_extp_integration.py
```

### Option 2: Validation Script
```bash
python validate_cus_extp_inputs.py
```

### Option 3: Production Test
```bash
python AdvancedTestExecutor.py
```

## Troubleshooting

### Issue: CUS Not Detecting ExtP
- **Check**: ExtP window is visible and active
- **Check**: ExtP shows expected prompts
- **Check**: CUS simulation_dictionary.txt has correct triggers

### Issue: CUS Not Sending Inputs
- **Check**: Keyboard simulation is working
- **Check**: CUS has proper window focus
- **Check**: No conflicting applications

### Issue: False Negatives Not Detected
- **Check**: Enhanced CUS is running
- **Check**: Remediation system is active
- **Check**: False negative patterns are in dictionary

### Issue: False Positive Error Detection
- **Cause**: OCR misreading file paths, VS Code interface, or help text
- **Solution**: CUS now automatically filters common false positives
- **Examples**: "GitRepos" misread as "error", file paths containing error-like words
- **Check**: Look for "⚡ FILTERED FALSE POSITIVE" messages in CUS logs

## Expected Results

### ✅ Working System Should Show:
1. CUS detects ExtP prompts within 2-3 seconds
2. CUS sends appropriate keyboard inputs
3. ExtP responds correctly to CUS inputs
4. False negatives are detected and remediated
5. System continues monitoring for new triggers

### 📊 Performance Metrics:
- **Trigger Detection**: < 3 seconds response time
- **Input Simulation**: Immediate key press after detection
- **False Negative Detection**: 95% confidence level
- **Remediation Success**: 100% effectiveness

## Log Files to Monitor

- `Logs/CUSEvents/` - CUS event logs
- `Logs/Screenshots/` - Screen capture logs
- `NewErrors/` - Error event files
- `TestResults/` - Test execution results
- `RemediationResults/` - Remediation action logs

## Quick Commands Reference

```bash
# Basic test
python CUS.py

# Enhanced test with remediation
python EnhancedCUS.py

# Full validation
python ProductionValidationTest.py

# Status check
python production_status_check.py

# Quick integration test
.\test_cus_extp_quick.bat
```
