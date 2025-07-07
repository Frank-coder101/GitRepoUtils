# CUS Project Code Archive

**Archive Date**: 2025-07-07  
**Reason**: Post-confirmation cleanup after successful Alt+Tab mode implementation

## What Works (Production Solution)

### ✅ **Production Files** (Kept in main directory)
- `CUS.py` - **FINAL VERSION** using Alt+Tab focus only
- `requirements.txt` - Clean dependencies (removed pywin32, added pyperclip)
- `simulation_dictionary.txt` - Trigger definitions
- `setup_test_environment.bat` - Comprehensive setup script
- `test_deps_minimal.py` - Dependency checker for Alt+Tab mode
- `requirements_minimal.txt` - Minimal Alt+Tab requirements

### ✅ **What Worked and Why**
1. **Alt+Tab Focus Method**: `pyautogui.hotkey('alt', 'tab')` 
   - Simple, reliable, works with any window arrangement
   - No complex window detection needed
   - No pywin32 dependencies required

2. **Multi-Method Input**: Fallback chain for reliability
   - pynput → pyautogui → Windows API → clipboard
   - Ensures actions work even if one method fails

3. **System Python**: Removed all venv complexity
   - Simpler deployment and maintenance
   - Direct system package management

## What Didn't Work (Archived)

### ❌ **Failed Approaches** → `failed_approaches/`
- **pywin32-based focusing**: Complex, unreliable, dependency-heavy
- **Window pattern matching**: Brittle, slow, over-engineered  
- **Virtual environments**: Added complexity without benefit
- **Full mode vs Alt+Tab modes**: Unnecessary branching

### 🧪 **Experimental Versions** → `experimental_versions/`
- Multiple CUS variants (CUS_*.py files)
- Different approaches to the same problem
- Good for exploring solutions, but confusing after decision made

### 🧪 **Test Experiments** → `test_experiments/`
- Dozens of test files exploring different aspects
- Validation scripts for various approaches
- Useful during development, noise after confirmation

### 📜 **Legacy Code** → `legacy_code/`
- Old configuration files and unused scripts
- Backup versions and alternative implementations

## Key Insights for Future Development

1. **Alt+Tab is sufficient** for window focusing in automation
2. **Multi-method fallbacks** are critical for input reliability  
3. **System Python** is simpler than virtual environments for tools like this
4. **One working solution** is better than multiple complex options
5. **User confirmation** is the trigger for cleanup, not AI assessment

## Dependencies Evolution

**Before Cleanup**:
```
- pywin32 (complex window management)
- Multiple experimental requirements files
- Virtual environment setup
```

**After Cleanup**:
```
- pyperclip (clipboard operations)
- Simple system Python dependencies
- Single requirements.txt
```

## Architecture Decision

**DECISION**: Alt+Tab-only mode is the production approach
**REASONING**: 
- Passed all user tests
- Simple and reliable
- Minimal dependencies
- Easy to maintain

---
*This archive preserves development history while keeping production environment clean.*
